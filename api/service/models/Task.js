const mongoose = require('mongoose');

const TaskSchema = mongoose.Schema({
    subject_id: Number,
    task_text: String
});

module.exports = mongoose.model('Task', TaskSchema);