import os
import pickle
from flask import Flask, render_template, request, send_from_directory, jsonify
from predict import create_midi, prepare_sequences, create_network, generate_notes

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top

DATA_DIRECTORY = os.path.join(APP_ROOT, "lstmresources\\notedata")
MODEL_DIRECTORY = os.path.join(APP_ROOT,"lstmresources\\savedModel")
GENERATED_MUSIC_DIRECTORY = os.path.join(APP_ROOT,"generatedMusic")
DEFAULT_MUSIC = "default.mid"

@app.route("/")
@app.route("/index.html")
def home():
    return render_template("index.html")

@app.route("/generate")
def generate():
    genre = request.args.get("genre", default="finalfantasy", type=str)
    filename = request.args.get("filename", type=str)
    diversity = float(request.args.get("diversity"))
    noteslength = int(request.args.get("noteslength"))

    """ Generate a piano midi file """
    #load the notes used to train the model
    with open(os.path.join(DATA_DIRECTORY, genre), 'rb') as filepath:
        notes = pickle.load(filepath)

    # Get all pitch names
    pitchnames = sorted(set(item for item in notes))
    # Get all pitch names
    n_vocab = len(set(notes))

    network_input, normalized_input = prepare_sequences(notes, pitchnames, n_vocab)
    model = create_network(normalized_input, n_vocab, genre, weightdir = os.path.join(MODEL_DIRECTORY, genre+".hdf5"))
    prediction_output = generate_notes(model, network_input, pitchnames, n_vocab, diversity, noteslength)
    midi_stream = create_midi(prediction_output)

    filepath = os.path.join(GENERATED_MUSIC_DIRECTORY, filename+".mid")

    midi_stream.write("midi", fp=filepath)

    if filepath is not None:
        return jsonify({"status":"success", "generatedfilepath" : os.path.join(GENERATED_MUSIC_DIRECTORY, filepath)})
    else:
        return jsonify({"status":"failure", "generatedfilepath" : DEFAULT_MUSIC})

@app.route("/files/<path:path>")
def download_file(path):
    return send_from_directory(GENERATED_MUSIC_DIRECTORY, path, as_attachment=True)

@app.route("/files/<filename>", methods=["POST"])
def upload_file(filename):
    if "/" in filename:
        return jsonify({"success":"false"})
    try:
        with open(os.path.join(GENERATED_MUSIC_DIRECTORY, filename), "wb") as fp:
            fp.write(request.data)
        return jsonify({"success":"true"})
    except:
        return jsonify({"success":"false"})


@app.route("/files")
def list_files():
    """Endpoint to list files on the server."""
    files = []
    for filename in os.listdir(GENERATED_MUSIC_DIRECTORY):
        path = os.path.join(GENERATED_MUSIC_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return jsonify(files)

app.run(debug=True, port=8080)