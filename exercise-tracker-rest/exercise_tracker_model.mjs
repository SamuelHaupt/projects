import mongoose from 'mongoose';

// Prepare the database exercise_tracker_app_db in the MongoDB
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
const Exercise = mongoose.model('Exercise', exerciseSchema)

