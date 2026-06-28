const { useState, useEffect } = React;


const mockActivities = [
    // fetch("/api/activity-feed/")
    {
        id: 1,
        icon: "💰",
        title: "Deposit Completed",
        message: "₦50,000 added to wallet",
        type: "success"
    },
    {
        id: 2,
        icon: "📈",
        title: "Bitcoin Rising",
        message: "+4.2% today",
        type: "info"
    },
    {
        id: 3,
        icon: "🚗",
        title: "Vehicle Dividend",
        message: "₦3,500 received",
        type: "reward"
    }
];

function ActivityCard({
    activity,
    index,
    removeActivity
}) {
    const [expanded, setExpanded] = useState(false);

    const offset = index * 14;
    // const scale = 1 - (index * 0.05);
    const scale = 1 - offset;

    return (
        <div
            className={`activity-card ${expanded ? 'expanded' : ''}`}
            style={{
                bottom: `${offset}px`,
                transform: `scale(${scale})`,
                zIndex: 100 - index
            }}
            onClick={() => setExpanded(!expanded)}
        >

            <div className="activity-header">

                <div className="activity-left">

                    <span className="activity-icon">
                        {activity.icon}
                    </span>

                    <div>

                        <div className="activity-title">
                            {activity.title}
                        </div>

                        <div className="activity-message">
                            {activity.message}
                        </div>

                    </div>

                </div>

                <button
                    className="close-btn"
                    onClick={(e) => {
                        e.stopPropagation();
                        removeActivity(activity.id);
                    }}
                >
                    ✕
                </button>

            </div>

            {expanded && (
                <div className="activity-body">

                    <div className="activity-tag">
                        {activity.type}
                    </div>

                    <div className="activity-time">
                        Just now
                    </div>

                </div>
            )}

        </div>
    );
}


function ActivityFeed() {

    const [activities, setActivities] = useState([]);

    useEffect(() => {

        let counter = 0;

        const interval = setInterval(() => {

            const nextActivity = mockActivities[counter];

            if (!nextActivity) {
                clearInterval(interval);
                return;
            }

            setActivities(prev => [
                nextActivity,
                ...prev
            ]);

            counter++;

        }, 2500);

        return () => clearInterval(interval);

    }, []);

    useEffect(() => {

        const timer = setInterval(() => {

            setActivities(prev => {

                if (prev.length <= 3) return prev;

                return prev.slice(0, prev.length - 1);

            });

        }, 8000);

        return () => clearInterval(timer);

    }, []);

    const removeActivity = (id) => {

        setActivities(prev =>
            prev.filter(item => item.id !== id)
        );

    };

    return (
        <div className="activity-feed-container">

            {
                activities
                    .filter(Boolean)
                    .slice(0, 3)
                    .map((activity, index) => (

                        <ActivityCard
                            key={activity.id}
                            activity={activity}
                            index={index}
                            removeActivity={removeActivity}
                        />

                    ))}

        </div>
    );
}

// function ActivityFeed() {

//     return (
//         <div
//             style={{
//                 position: "fixed",
//                 left: "20px",
//                 bottom: "20px",
//                 background: "red",
//                 color: "white",
//                 padding: "20px",
//                 zIndex: 99999,
//                 display: "flex",
//                 flexDirection: "row",
//                 // animation:
//             }}
//         >
//             Activity Feed Loaded <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
//                 <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
//             </svg>

//         </div>
//     );

// }


// const rootElement =
//     document.getElementById("activity-feed-root");

// if (rootElement) {

//     if (!window.activityFeedRoot) {

//         window.activityFeedRoot =
//             ReactDOM.createRoot(rootElement);

//     }

//     window.activityFeedRoot.render(
//         <ActivityFeed />
//     );
// }