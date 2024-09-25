# ViaVision

Via Vision uses OpenCV and YOLOv8 to detect traffic signs, make predictions about their location, and store those predictions in a PostgreSQL database, all while connecting to a custom Unreal Engine 5 project with web sockets. Theoretically, this architecture could be used by self driving cars, or other cars which capture images, to provide live updates to various map platforms. 
