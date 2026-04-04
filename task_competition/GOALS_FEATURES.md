# Weekly & Monthly Goals Features

## Overview
The Daily Task Competition application now includes a comprehensive weekly and monthly goals management system with timer functionality.

## Features

### 1. Goals System
- **Weekly Goals**: Track goals that reset every week
- **Monthly Goals**: Track goals that reset every month
- **Two Goal Types**:
  - **Completion-based**: Simple checkbox goals (e.g., "Write essay")
  - **Target-based**: Goals with a specific count target (e.g., "Read 7 papers")

### 2. Goal Management
- **Create Goals**: Add new weekly or monthly goals with custom points
- **Track Progress**: Visual progress bars for target-based goals
- **Complete Goals**: Mark goals as complete with one click
- **Increment Progress**: For target-based goals, increment progress count
- **Deadlines**: Optional start and end dates
- **Priority Levels**: Low, Medium, High priority indicators

### 3. Timer Functionality
- **Task Timers**: Add timers to specific tasks
- **Duration Tracking**: Set time limits for tasks (e.g., 60 minutes)
- **Start/Pause/Resume**: Full timer controls
- **Time Tracking**: Elapsed time saved with task completion
- **Visual Progress**: Progress bars showing time remaining
- **Warnings**: Audio/visual alerts at 5-minute mark
- **localStorage Persistence**: Timer state saved across page refreshes

### 4. Statistics Dashboard
- **Progress Overview**: See overall goal completion rate
- **Weekly Progress**: Detailed progress on all weekly goals
- **Monthly Progress**: Detailed progress on all monthly goals
- **Completion Rates**: Track how many goals are completed vs in-progress
- **Points Tracking**: See how many points earned from goals

### 5. Database Schema

#### Task Model Updates
```
- category: 'daily', 'weekly', or 'monthly'
- order: Task ordering within category
- duration_minutes: Time limit for task timer (0 = no timer)
- target: Count target for target-based goals (0 = checkbox only)
```

#### TaskCompletion Model Updates
```
- progress_count: Count of items completed toward target
- elapsed_seconds: Time spent on timed tasks
- completion_type: 'full' or 'partial' completion
- week_key: ISO week identifier for weekly goals
- month_key: Month identifier for monthly goals
```

## User Interface

### Navigation
- **Goals Dropdown** in navbar with links to:
  - Weekly Goals Dashboard
  - Monthly Goals Dashboard
  - Statistics

### Main Dashboard
- Quick buttons to access:
  - Weekly Goals
  - Monthly Goals
  - Statistics Dashboard

### Weekly/Monthly Goals Dashboard
- Week/month navigation buttons
- List of all goals with progress bars
- Complete/Increment buttons for each goal
- Quick-action buttons

### Create Goal Form
- Title and description
- Goal type selection (completion or target)
- Target count input (for target-based goals)
- Duration in minutes (for timer)
- Points reward
- Optional start/end dates
- Priority level selector

### Timer UI
- Large digital timer display (HH:MM:SS)
- Progress bar filling as time passes
- Start/Pause/Stop/Reset buttons
- Time remaining display
- Automatic notifications at milestones

### Statistics Page
- Summary cards showing:
  - Total goals
  - Completed goals
  - In-progress goals
  - Completion rate percentage
- Tables for weekly and monthly progress
- Quick links back to goal dashboards

## Routes

### Goals Blueprint (`/goals`)
- `GET /goals/weekly` - Weekly dashboard
- `GET /goals/monthly` - Monthly dashboard
- `POST /goals/create/<type>` - Create new goal
- `POST /goals/<id>/complete` - Mark goal complete
- `POST /goals/<id>/progress` - Update progress (JSON)
- `GET /goals/statistics` - Statistics dashboard

### Tasks Blueprint (Timer endpoints)
- `POST /tasks/<id>/timer/start` - Start timer
- `POST /tasks/<id>/timer/pause` - Pause timer
- `POST /tasks/<id>/timer/stop` - Stop and save completion
- `POST /tasks/<id>/timer/reset` - Reset timer

## Design & Styling

### Dark Theme
- Full dark theme support for goals pages
- Green terminal-style dark theme option
- Responsive design for mobile
- Accessible color contrast

### Timer Styling
- Gradient backgrounds (purple → blue)
- Warning states (orange) when near time limit
- Danger state (red) when time expires
- Smooth animations and transitions
- Monospace font for timer display

## Client-Side Features

### TimerManager Class (JavaScript)
- Manages timer state and persistence
- localStorage persistence for timer state
- Automatic time tracking and updates
- Visual state updates (progress bars, time display)
- Button state management

### Features
- Format time to HH:MM:SS
- Track elapsed time
- Auto-start warnings
- Automatic stop on time expiration
- Drag-and-drop persistence

## Point System
- Complete weekly goal: +goal.points
- Complete monthly goal: +goal.points
- Each goal has configurable points
- Points added to user's total_points
- Displayed in real-time
- Tracked in leaderboard

## Best Practices

1. **Weekly Goals**: Use for recurring tasks that reset weekly (e.g., study goals)
2. **Monthly Goals**: Use for longer-term objectives (e.g., reading a book)
3. **Timers**: Useful for tasks with time constraints
4. **Progress Tracking**: Set reasonable targets (e.g., 7 items per week)
5. **Points**: Higher points = more challenging goals

## Technical Implementation

### Backend
- Flask Blueprints for modular routes
- SQLAlchemy ORM for data persistence
- Flask-Login for authentication
- JSON API for AJAX calls
- Proper date handling with ISO week/month keys

### Frontend
- Bootstrap 5 for responsive UI
- Vanilla JavaScript (no jQuery)
- localStorage for client persistence
- Real-time progress updates
- Smooth animations and transitions

### Database
- Cascade deletes for cleanup
- Unique constraints for data integrity
- Proper foreign key relationships
- Indexed queries for performance

## Future Enhancements
- Goal templates/presets
- Recurring goal patterns
- Goal sharing with other users
- Detailed analytics and charts
- Goal history and achievements
- Reminder notifications
- Goal categories and tags
- Integration with calendar view
