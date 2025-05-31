import type { ReactNode } from 'react';
import '../styles/heromessage.css'

type HeroMessageProps = {
    title: ReactNode;
    subMessage: string;
    buttonText: string;
};

function HeroMessage({ title, subMessage, buttonText }: HeroMessageProps) {
    return (
        <div className='message'>
            <h1>{title}</h1>
            <p>{subMessage}</p>
            <a href="/signup">
            <button>{buttonText}</button>
            </a>
        </div>
    );
}

export default HeroMessage;