def move_to_room(room, currentroom):
    import time

    with open('bot_status.txt', 'r') as f:
        content = f.read()
        modified_content = 'moving ' + content.split(' ', 1)[-1]
    with open('bot_status.txt', 'w') as f:
        f.write(modified_content)
    # bedroom 1 to charging station
    if currentroom == "bedroom1" and room == "charging_station":
        time.sleep(5)
        print(f"Moving to charging_station from bedroom1")
    # bedroom 1 to living room
    elif currentroom == "bedroom1" and room == "living_room":
        time.sleep(5)
        print(f"Moving to living_room from bedroom1")
    # bedroom 1 to bedroom 2  
    elif currentroom == "bedroom1" and room == "bedroom2":
        time.sleep(5)
        print(f"Moving to bedroom2 from bedroom1")
    # living room to bedroom 1
    elif currentroom == "living_room" and room == "bedroom1":
        time.sleep(5)
        print(f"Moving to bedroom1 from living_room")
    # living room to charging station
    elif currentroom == "living_room" and room == "charging_station":
        time.sleep(5)
        print(f"Moving to charging_station from living_room")
    # living room to bedroom 2
    elif currentroom == "living_room" and room == "bedroom2":
        time.sleep(5)
        print(f"Moving to bedroom2 from living_room")
    # bedroom 2 to living room
    elif currentroom == "bedroom2" and room == "living_room":
        time.sleep(5)
        print(f"Moving to living_room from bedroom2")
    # bedroom 2 to bedroom 1
    elif currentroom == "bedroom2" and room == "bedroom1":
        time.sleep(5)
        print(f"Moving to bedroom1 from bedroom2")
    # bedroom 2 to charging station
    elif currentroom == "bedroom2" and room == "charging_station":
        time.sleep(5)
        print(f"Moving to charging_station from bedroom2")
    # charging station to bedroom 1
    elif currentroom == "charging_station" and room == "bedroom1":
        time.sleep(5)
        print(f"Moving to bedroom1 from charging_station")
    # charging station to living room
    elif currentroom == "charging_station" and room == "living_room":
        time.sleep(5)
        print(f"Moving to living_room from bedroom2")
    # charging station to bedroom 2
    elif currentroom == "charging_station" and room == "bedroom2":
        time.sleep(5)
        print(f"Moving to bedroom2 from charging_station")
    with open('bot_status.txt', 'w') as f:
        f.write(f"ready {room}")
  
def park():
    print("bot now parked")