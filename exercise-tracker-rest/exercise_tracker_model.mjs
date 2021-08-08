import mongoose from 'mongoose';

// Prepare the database exercise_tracker_db in the MongoDB
// server running locally on port 27017.
mongoose.connect(
    'mongodb://localhost:27017/exercise_tracker_db',
    { useNewUrlParser: true, useUnifiedTopology: true }
);

// Connect to the database.
const database = mongoose.connection;
// Establishes event upon initial opening and logs successful connection.
database.once('open', () => {
    console.log('Successfully connected to MongDb using Mongoose!')
});

// Indexes used with faster querying.
mongoose.set('useCreateIndex', true);

/**
 * Define schema.
 */
const exerciseSchema = mongoose.Schema({
    name: {type: String, required: true},
    repetitions: {type: Number, required: true},
    weight: {type: Number, required: true},
    unitMeasurement: {type: String, required: true},
    date: {type: String, required: true} // Must be in format 'MM-DD-YY'.
});

/**
 * Compiles model from schema.
 */
const Exercise = mongoose.model('Exercise', exerciseSchema);

/**
 * Creates an exercise.
 * @param {String} name
 * @param {Number} repetitions
 * @param {Number} weight
 * @param {String} unitMeasurement
 * @param {String} date
 * @returns a promise. Resolves to JSON object.
 */
const createExercise = async (name, repetitions, weight, unitMeasurement, date) => {
    const exercise = new Exercise({ name: name,
                                    repetitions: repetitions,
                                    weight: weight,
                                    unitMeasurement: unitMeasurement,
                                    date: date });
    return exercise.save(); // Persists resource to exercise_tracker_db.
}

/**
 * Retrieves all exercises in database. No filters are passed.
 */
const retrieveAllExercises = async () => {
    const query = Exercise.find({}); // Passes empty object to return all exercises.
    return query.exec(); // Executes query on database.
}

export {createExercise, retrieveAllExercises};