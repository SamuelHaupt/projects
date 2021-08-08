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
 * Create new exercise.
 * {endpoint: create}
 */
app.post('/exercises', (request, response) => {
    exercises.createExercise(   request.body.name,
                                request.body.repetitions,
                                request.body.weight,
                                request.body.unitMeasurement,
                                request.body.date)
        .then(exercise => {
            // Sets status code to 'Created': 201.
            response.status(201).json(exercise);
        })
        .catch(error => {
            console.error(error);
            // Sets status code to 'Bad Request': 400.
            // Future expansion: Include code to test error and set 
            // status code accordingly.
            response.status(400).json({Error: 'Request failed.'});
        });
});

/** 
 * Retrieve all exercises.
 * {endpoint: retrieve}
 */
app.get('/exercises', (request, response) => {
    exercises.retrieveAllExercises()
        .then(exercises => {
            // Sets status code automatically to 'OK': 200.
            response.json(exercises); 
        })
        .catch(error => {
            console.error(error);
            // Sets status code to 'Bad Request': 400.
            response.status(400).json({Error: 'Request failed.'});
        });
});

/**
 * Updates the exercise whose id is provided.
 * Requires all parameters for successful update.
 * {endpoint: update}
 */
app.put('/exercises/:id', (request, response) => {
    exercises.updateExercise(request.params._id, request.body)
        .then(result => {
            if (result.nModified === 1) {
                response.json({
                    _id: request.params._id,
                    name: request.body.name,
                    repetitions: request.body.repetitions,
                    weight: request.body.weight,
                    unitMeasurement: request.body.unitMeasurement,
                    date: request.body.date
                });
            } else {
                // Sets status code to 'Not Found': 404.
                response.status(404).json({Error: 'Resource not found'});
            }
        })
        .catch(error => {
            console.error(error);
            // Sets status code to 'Bad Request': 400.
            response.status(400).json({Error: 'Request failed.'});
        });
});