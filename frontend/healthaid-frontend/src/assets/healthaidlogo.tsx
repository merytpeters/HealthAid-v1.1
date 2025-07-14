function HealthaidLogo({ textColor = "#2C7A7B" }) {
  return (
    <svg
      width="200"
      height="50"
      viewBox="120 50"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Stylized medical cross */}
      <rect x="22" y="10" width="12" height="33" fill="#F56565" rx="3" />
      <rect x="12" y="22" width="33" height="12" fill="#F56565" rx="3" />

      {/* Accent small circle on top right as a subtle highlight */}
      <circle cx="40" cy="15" r="6" fill="#F56565" />

      {/* Brand name text in Secondary color (Soft Mint) */}
      <text
        x="60"
        y="35"
        fill={textColor}
        fontSize="24"
        fontWeight="600"
        fontFamily="Segoe UI, Tahoma, Geneva, Verdana, sans-serif"
      >
        HealthAid
      </text>
    </svg>
  );
}

export default HealthaidLogo;
