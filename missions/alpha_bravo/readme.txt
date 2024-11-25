An example mission of two vehicles waiting for waypoint information from HARMONY.

Setup: 
	expects pymoos.so file to be present in HARMONY folder

Usage: 
	Use launch_harmony.sh to launch HARMONY app alongside shore-side and vehicles. 

	launch.sh will launch without HARMONY
	
	inject_survey.sh will send the SURVEY_AREA message to shore-side app. HARMONY app is waiting for this message to start the generating waypoint info. 
