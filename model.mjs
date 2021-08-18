import mongoose from 'mongoose';

// username:password can be found under database acces on MongoDB Atlas Cloud.
// Set local to true if running app locally. Otherwise, keep false for running
// app on Heroku.
// Update password in environment variables on Heroku.
const MONGODB_URI = `mongodb+srv://user1:${process.env.MONGODB_PASSWORD}@exerciselogdb.3hic3.mongodb.net/myFirstDatabase?retryWrites=true&w=majority`;
const localTest = false;
const URI = process.env.MONGODB_URI;

// Prepare the database exercise_tracker_db in the MongoDB
// server running locally on port 27017.
mongoose.connect( URI || 'mongodb://localhost:27017/exercise_log_db', {
    useNewUrlParser: true,
    useUnifiedTopology: true
});

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
    reps: {type: Number, required: true},
    weight: {type: Number, required: true},
    unit: {type: String, required: true},
    date: {type: String, required: true} // Must be in format 'MM-DD-YY'.
});

/**
 * Compiles model from schema.
 */
const Exercise = mongoose.model('Exercise', exerciseSchema);

/**
 * Creates an exercise.
 * @param {String} name
 * @param {Number} reps
 * @param {Number} weight
 * @param {String} unit
 * @param {String} date
 * @returns a promise. Resolves to JSON object.
 */
const createExercise = async (name, reps, weight, unit, date) => {
    const exercise = new Exercise(
        {   name: name,
            reps: reps,
            weight: weight,
            unit: unit,
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
 * @param {Number} parameters.reps
 * @param {Number} parameters.weight
 * @param {String} parameters.unit
 * @param {String} parameters.date
 * @returns a promise, which includes properties: {n, nModified, ok}
 */
const updateExercise = async (_id, parameters) => {
    const result = await Exercise.replaceOne(
        {_id: _id}, 
        {   name: parameters.name,
            reps: parameters.reps,
            weight: parameters.weight,
            unit: parameters.unit,
            date: parameters.date},
        {omitUndefined: true, useFindAndModify: false}
    );
    return result.nModified;
}

/**
 * Deletes an exercise.
 * @param {String} _id
 * @returns a promise, which includes properties: {deletedCount}
 * deleteOne's result.deletedCount resolves to either 0 or 1.
 */
const deleteExercise = async (_id) => {
    const result = await Exercise.deleteOne({_id: _id});
    return result.deletedCount;
}

export {createExercise, retrieveAllExercises, updateExercise, deleteExercise};