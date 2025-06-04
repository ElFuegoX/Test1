from robot.explorer_robot import ExplorerRobot
from robot.delivery_robot import DeliveryRobot

def main():
    robo1 = ExplorerRobot("Scout-1")
    robo1.display_info()
    robo1.move()
    robo1.scan_area()
    robo1.display_info()

    print("\n-----------------\n")

    robo2 = DeliveryRobot("Carrier-1", destination=(10, 10))
    robo2.load("Colis A")
    robo2.move()
    robo2.unload()
    robo2.display_info()

if __name__ == "__main__":
    main()
