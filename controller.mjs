import express from 'express';
import morgan from 'morgan';
import * as exercises from './model.mjs';

const PORT = process.env.PORT || 8080;
const app = express();
app.use(express.json());


// HTTP request logger
app.use(morgan('tiny'));


/**
 * Create new exercise.
 * {endpoint: create}
 */
app.post('/exercises', (request, response) => {
    exercises.createExercise(   request.body.name,
                                request.body.reps,
                                request.body.weight,
                                request.body.unit,
                                request.body.date)
        .then(exercise => {
            // Sets status code to 'Created': 201.
            // 'content-type' is updated automatiicaly to 'application/json'.
            response.status(201).json(exercise);
        })
        .catch(error => {
            console.error(error);
            // Sets status code to 'Internal Server Error': 500.
            // Future expansion: Include code to test error and set 
            // status code accordingly.
            response.status(500).json({Error: 'Request failed.'});
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
            // 'content-type' is updated automaticaly to 'application/json'.
            response.json(exercises); 
        })
        .catch(error => {
            console.error(error);
            // Sets status code to 'Internal Server Error': 500.
            response.status(500).json({Error: 'Request failed.'});
        });
});


/**
 * Updates the exercise whose id is provided.
 * Requires all parameters for successful update.
 * {endpoint: update}
 */
app.put('/exercises/:_id', (request, response) => {
    exercises.updateExercise(request.params._id, request.body)
        .then(nModified => {
            if (nModified === 1) {
                // Sets status code automatically to 'OK': 200.
                // 'content-type' is updated automatiicaly to 'application/json'.
                response.json({
                    _id: request.params._id,
                    name: request.body.name,
                    reps: request.body.reps,
                    weight: request.body.weight,
                    unit: request.body.unit,
                    date: request.body.date
                });
            } else {
                // Sets status code to 'Not Found': 404.
                response.status(404).json({Error: 'Resource not found'});
            }
        })
        .catch(error => {
            console.error(error);
            // Sets status code to 'Internal Server Error': 500.
            response.status(500).json({Error: 'Request failed.'});
        });
});


/**
 * Deletes the exercise whose id is provided in the query parameters.
 */
app.delete('/exercises/:_id', (request, response) => {
    exercises.deleteExercise(request.params._id)
        .then(deletedCount => {
            if (deletedCount === 1) {
                // Sets status code automatically to 'No Content': 204.
                // Deletion was successful.
                response.status(204).send();
            } else {
                // Sets status code to 'Not Found': 404.
                response.status(404).json({Error: 'Resource not found'});
            }
        })
        .catch(error => {
            console.error(error);
            // Sets status code to 'Internal Server Error': 500.
            response.status(500).json({Error: 'Request failed.'});
        });
});


// Redirects Heroku to use client_view/build when in production.
if (process.env.NODE_ENV === 'production') {
    app.use(express.static('client_view/build'))
}


app.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}.`)
});