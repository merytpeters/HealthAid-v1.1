import { useEffect, useState } from "react";
import HealthaidLogo from "../assets/healthaidlogo";
import '../styles/landing.css';
import GlobalHeader from "../components/globalheader";
import HeroMessage from "../components/heroMessage";
import Content from "../components/contentSection";
import Footer from "../components/footer";

function Landing() {
  const [animate, setAnimate] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setAnimate(true);
    }, 100); // Delay for CSS transition

    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="landing-container">
      <div className="hero">
        <section id="section1">
        <div className={`logo ${animate ? "animate" : ""}`}>
          <HealthaidLogo />
        </div>
        </section>

        <div className={`page-content ${animate ? "show" : ""}`}>
          <GlobalHeader />

          <section id="section2">
          <div className="hero-content">
            <div className="hero-message">
              <HeroMessage
                title={
                  <>
                    Managing <br />
                    Chronic Diseases <br />
                    with Ease
                  </>
                }
                subMessage="Smarter health, better days."
                buttonText="Get Started"
              />
            </div>
            <div className="hero-image">
              <div className="hero-image-wrapper">
                <div className="circle-bg"></div>
                <img src="/img/heroimage.png" alt="hero" />
              </div>
            </div>
          </div>
          </section>
        

          <section id="section3">
          <div className="content-section">
            <Content />
          </div>
          </section>
        </div>
      </div>

      <section id="section4">
      <div className="footer">
        <Footer />
      </div>
      </section>
    </div>
  );
}

export default Landing;

