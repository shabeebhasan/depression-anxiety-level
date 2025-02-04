import modulefinder

finder = modulefinder.ModuleFinder()
finder.run_script("real_time_video.py")
print(finder.modules.keys())