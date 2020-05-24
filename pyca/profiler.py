import cProfile
import pstats
try:
    from StringIO import StringIO ## for Python 2
except ImportError:
    from io import StringIO ## for Python 3


def qprofile(func):
    def profiled_func(*args, **kwargs):
        if 'profile' in kwargs and kwargs['profile']:
            kwargs.pop('profile')
            profile = cProfile.Profile()
            try:
                profile.enable()
                result = func(*args, **kwargs)
                profile.disable()
                return result
            finally:
                s = StringIO()
                ps = pstats.Stats(
                    profile, stream=s).strip_dirs(
                ).sort_stats('cumulative')
                ps.print_stats(30)
                print(s.getvalue())
        else:
            result = func(*args, **kwargs)
            return result
    return profiled_func