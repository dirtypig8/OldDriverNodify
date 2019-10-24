import traceback
import sys
from ArgParser import ArgParser
from LogWriter import LogWriter
from SystemInitializer.StartServing import StartServing
from SystemInitializer.InitializeLogWritter import InitializeLogWriter
from SystemInitializer.InitializeConfigDictionary import InitializeConfigDictionary



if __name__ == '__main__':
    exit_code = 0
    try:
        commandline_args = ArgParser().get_args()
        InitializeConfigDictionary().execute(commandline_args.config_path)
        InitializeLogWriter().execute()
        StartServing().execute()

    except Exception:
        error_traceback = traceback.format_exc()
        LogWriter().write_log(error_traceback)
        exit_code = 2

    finally:
        LogWriter().write_log("exit program...")
        sys.exit(exit_code)