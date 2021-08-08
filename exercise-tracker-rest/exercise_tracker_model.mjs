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
    const exercise = new Exercise(
        {   name: name,
            repetitions: repetitions,
            weight: weight,
            unitMeasurement: unitMeasurement,
            date: date}
    );
    return exercise.save(); // Persists resource to exercise_tracker_db.
}

/**
 * Retrieves all exercises in database. No filters are passed.
 * @param
 * @returns
 */
const retrieveAllExercises = async () => {
    const query = Exercise.find({}); // Passes empty object to return all exercises.
    return query.exec(); // Executes query on database.
}

/**
 * Updates an exercise.
 * @param {String} _id
 * @param {String} parameters.name
 * @param {Number} parameters.repetitions
 * @param {Number} parameters.weight
 * @param {String} parameters.unitMeasurement
 * @param {String} parameters.date
 * @returns a promise, which includes properties: {n, nModified, ok}
 */
const updateExercise = async (_id, parameters) => {
    const result = await Exercise.findByIdAndUpdate(
        {_id: _id}, 
        {   name: parameters.name,
            repetitions: parameters.repetitions,
            weight: parameters.weight,
            unitMeasurement: parameters.unitMeasurement,
            date: parameters.date},
        {omitUndefined: true, useFindAndModify: false}
    );
    return result;
}

export {createExercise, retrieveAllExercises, updateExercise};