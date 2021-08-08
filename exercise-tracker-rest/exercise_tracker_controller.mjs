import express from 'express';

const PORT = 3000;

const app = express();

app.use(express.static('public'));

app.use(express.urlendcoded({
    extended: true
}));

app.use(express.json());