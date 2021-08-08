import express from 'express';
import * as exercises from './exercise_tracker_model.mjs';

const PORT = 3000;

const app = express();
app.use(express.static('public'));
app.use(express.urlendcoded({
    extended: true
}));
app.use(express.json());

/**
 * New exercise endpoint. Create new exercise.
 */
app.post('/exercises', (request, response) => {
    exercises.createExercise(   request.body.name,
                                request.body.repetitions,
                                request.body.weight,
                                request.body.unitMeasurement,
                                request.body.date)
        .then(exercise => {
            // Sets status code to 'created': 201.
            response.status(201).json(exercise);
        })
        .catch(error => {
            console.error(error);
            // Sets status code to 'bad request': 400.
            // Future expansion: Include code to test error and set 
            // status code accordingly.
            response.status(400).json({Error: 'Request failed.'});
        });
});