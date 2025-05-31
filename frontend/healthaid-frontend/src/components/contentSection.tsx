import '../styles/content.css';

function Content() {
const features = [
  {
    icon: "💡",
    title: "Symptom Checker",
    description:
      "Quickly identify potential conditions based on your symptoms using AI-powered insights.",
  },
  {
    icon: "💊",
    title: "Medication Tracking",
    description:
      "Keep a daily log of your prescriptions, dosages, and schedules effortlessly.",
  },
  {
    icon: "📈",
    title: "Health Insights",
    description:
      "Visualize trends and analytics around your health data to make informed decisions.",
  },
  {
    icon: "⏰",
    title: "Pill Reminder",
    description:
      "Get timely notifications so you never miss a dose again.",
  },
  {
    icon: "📝",
    title: "Symptom Journal",
    description:
      "Log your daily symptoms to monitor changes and share accurate reports with your healthcare provider.",
  },
  {
    icon: "💬",
    title: "Drug Interaction Checker",
    description:
      "Ensure your medications are safe to take together with real-time interaction alerts.",
  },
  {
    icon: "📦",
    title: "Inventory System",
    description:
      "Track your medication supply and receive alerts when you're running low.",
  },
  {
    icon: "📚",
    title: "First Aid Guide",
    description:
      "Access quick first aid instructions for emergencies and common health issues.",
  }
];

  return (
    <div id="features" className="content-container">
      <h2>Features</h2>

      <div className="feature-content">
        <ul>
          {features.map((feature, index) => (
            <li key={index}>
              <h3>
                {feature.icon} {feature.title}
              </h3>
              <p>{feature.description}</p>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default Content;