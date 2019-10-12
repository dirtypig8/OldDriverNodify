import traceback
from ArgParser import ArgParser
from SystemInitializer.InitializeConfigDictionary import InitializeConfigDictionary
from SystemInitializer.StartServing import StartServing


if __name__ == '__main__':
    exit_code = 0
    try:
        commandline_args = ArgParser().get_args()
        InitializeConfigDictionary().execute(commandline_args.config_path)
        # InitializeLogWriter().execute()
        StartServing().execute()

    except Exception:
        error_traceback = traceback.format_exc()
        print("Main error")
        # LogWriter().write_log(error_traceback)
        exit_code = 2

    finally:
        # LogWriter().write_log("exit program...")
        exit(exit_code)