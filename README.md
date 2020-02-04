# Homework Telegram Bot
Development cycle groups (for branches naming)
- `feature/feature-name` - for new features and functionalities
- `bug/bug-name` - for bug being fixed
- `hotfix/bug-name` - hotfix for known bug that must be refactored as soon as possible
- `development` - draft branch for the last tests before merging to master
- `junk/test-name` - for tests and experiments; must be deleted after work is complete
#
### For now bot only has telegram interface, but web version is planned.
### Commands:
- `/new_chat` - creates new chat entity in database
- `/subjects` - sends list of all subjects for current chat
- `/done` - informs bot that user is done with sending attachments (photos or docs)

### Commands if debug mode is enabled:
- `/chat_id` - sends current `chat_id`
- `/file <file_id>` - sends file with specific `<file_id>`
#### To get `file_id` of specific photo send it with caption "/file_id"

