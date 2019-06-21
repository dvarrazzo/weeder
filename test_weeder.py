import io
import re
import datetime as dt

from weeder import Weeder, run_cmdline


def test_default_policy_progression():
    files = []

    # Simulate running across a period
    for i in range(2000):
        d = dt.date(2000, 1, 1) + dt.timedelta(days=i)
        files.append("dir/file-%s.ext" % d)
        w = Weeder(files, refdate=d)
        for f in w.get_files_to_delete():
            files.remove(f)

    def f2d(fn):
        m = re.search(r"(\d{4})-(\d{2})-(\d{2})", fn)
        return dt.date(*[int(g) for g in m.groups()])

    all_dates = [f2d(fn) for fn in files]
    df = dt.date(2000, 1, 1) + dt.timedelta(days=1999)

    for d1, d0, dist in (
        (0, 14, 1),
        (14, 84, 7),
        (84, 364, 28),
        (364, 10000, 364),
    ):
        dist = dt.timedelta(days=dist)
        d0 = df - dt.timedelta(days=d0)
        d1 = df - dt.timedelta(days=d1)

        dates = [x for x in all_dates if d0 <= x < d1]
        assert dates
        for i in range(len(dates) - 1):
            assert dates[i + 1] - dates[i] == dist


def files1():
    dates = [dt.date.today() - dt.timedelta(days=i) for i in range(50)]
    dates.reverse()
    files = ["dir/file-%s.ext" % d for d in dates]
    return files


def weed(args, files):
    out = io.StringIO()
    run_cmdline(args=args + files, outfile=out)
    out = out.getvalue().splitlines()
    return out


def check1(files, left):
    assert len(left) < len(files)

    # All files kept in the last 2 weeks
    assert left[-14:] == files[-14:]

    def d(fn):
        return dt.datetime.strptime(fn, 'dir/file-%Y-%m-%d.ext')

    # One file every week in the first days
    for i in range(5):
        assert d(left[i + 1]) - d(left[i]) == dt.timedelta(days=7)


def test_cmdline_default():
    files = files1()
    out = weed([], files)
    left = sorted(set(files) - set(out))
    check1(files, left)


def test_cmdline_goners():
    files = files1()
    out = weed(['--print-goners'], files)
    left = sorted(set(files) - set(out))
    check1(files, left)


def test_cmdline_keepers():
    files = files1()
    left = weed(['--print-keepers'], files)
    check1(files, left)
