const mongoose = require('mongoose');

const SubjectSchema = mongoose.Schema({
    chat_id: Number,
    subject_name: String
});

module.exports = mongoose.model('Subject', SubjectSchema);