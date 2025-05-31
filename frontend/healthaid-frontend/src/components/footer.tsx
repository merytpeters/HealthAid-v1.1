function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer style={{ backgroundColor: '#0F4C5C', color: 'white', padding: '2rem 1rem' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto', display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between' }}>
        
        {/* Brand Info */}
        <div style={{ flex: '1 1 250px', marginBottom: '1rem' }}>
          <h3 style={{ marginBottom: '0.5rem' }}>HealthAid</h3>
          <p style={{ fontSize: '0.9rem' }}>
            Smarter tools for managing <br />
            chronic diseases. <br />
            Empowering better health, <br />
            one step at a time.
          </p>
        </div>

        {/* Navigation Links */}
        <div style={{ flex: '1 1 150px', marginBottom: '1rem' }}>
          <h4>Company</h4>
          <ul style={{ listStyle: 'none', padding: 0 }}>
            <li><a href="/about" style={linkStyle}>About Us</a></li>
            <li><a href="/contact" style={linkStyle}>Contact</a></li>
            <li><a href="/careers" style={linkStyle}>Careers</a></li>
          </ul>
        </div>

        {/* Legal Links */}
        <div style={{ flex: '1 1 150px', marginBottom: '1rem' }}>
          <h4>Legal</h4>
          <ul style={{ listStyle: 'none', padding: 0 }}>
            <li><a href="/privacy" style={linkStyle}>Privacy Policy</a></li>
            <li><a href="/terms" style={linkStyle}>Terms of Service</a></li>
          </ul>
        </div>

        {/* Social Media */}
        <div style={{ flex: '1 1 150px', marginBottom: '1rem' }}>
          <h4>Connect</h4>
          <ul style={{ listStyle: 'none', padding: 0 }}>
            <li><a href="https://twitter.com" target="_blank" rel="noopener noreferrer" style={linkStyle}>Twitter</a></li>
            <li><a href="https://linkedin.com/in/edafemerit" target="_blank" rel="noopener noreferrer" style={linkStyle}>LinkedIn</a></li>
            <li><a href="https://instagram.com" target="_blank" rel="noopener noreferrer" style={linkStyle}>Instagram</a></li>
          </ul>
        </div>
      </div>

      {/* Bottom Line */}
      <div style={{ textAlign: 'center', marginTop: '2rem', borderTop: '1px solid #2D3748', paddingTop: '1rem', fontSize: '0.85rem' }}>
        &copy; {currentYear} HealthAid. All rights reserved.
      </div>
    </footer>
  );
}

// Shared style for links
const linkStyle = {
  color: '#E6FFFA',
  textDecoration: 'none',
  fontSize: '0.9rem',
};

export default Footer;
