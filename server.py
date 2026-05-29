import json
import zmq

PORT = 5557

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind(f"tcp://*:{PORT}")

print(f"Microservice started on port {PORT}...")
coursePar = 0
numberStrokes = 0
golfRank = ""

while True:
    # Receive the course par and number of strokes as raw bytes
    rawBytes = socket.recv()

    print(f"Received raw bytes: {rawBytes}")

    try:
        # Parse the bytes to a string
        jsonData = json.loads(rawBytes.decode('utf-8'))

        # Extract the course par from the wrapper
        coursePar = int(jsonData["coursePar"])

        # Extract the number of strokes from the wrapper
        numberStrokes = float(jsonData["numberStrokes"])

        strokesMinusPar = numberStrokes - coursePar

        # Determine rank
        match strokesMinusPar:
            case x if x < -1:
                golfRank = f"{abs(x)} strokes under par."
            case -1:
                golfRank = f"Birdie. {abs(x)} strokes under par."
            case 0:
                golfRank = f"Par. {abs(x)} strokes."
            case 1:
                golfRank = f"Bogey. {abs(x)} strokes over par."
            case 2:
                golfRank = f"Double bogey. {abs(x)} strokes over par."
            case 3:
                golfRank = f"Triple bogey. {abs(x)} strokes over par."
            case _:
                golfRank = f"{abs(x)} strokes over par."

    except Exception as err:
        print(f"Parsing error: {err}")

    # Pack the golf rank into JSON structure
    responseDict = {"golfRank": golfRank}
    responseJsonString = json.dumps(responseDict)

    # Send the JSON string back to Unity encoded as bytes
    socket.send(responseJsonString.encode('utf-8'))