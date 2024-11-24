import React, { useEffect } from 'react';
import '../styles/StyleLoadingPage.scss';
import { Link, useNavigate } from 'react-router-dom';

function LoadingPage() {
    const navigate = useNavigate();

    useEffect(() => {
        const checkForSourceId = async () => {
            try {
                const response = await fetch('/results.json');
                if (response.ok) {
                    const data = await response.json();
                    if (JSON.stringify(data).includes('sourceid')) {
                        navigate('/vulnerabilities'); // Перенаправляємо на іншу сторінку
                    }
                }
            } catch (error) {
                console.error('Error fetching results.json:', error);
            }
        };

        const interval = setInterval(checkForSourceId, 3000); // Перевіряємо кожні 3 секунди

        return () => clearInterval(interval); // Очищаємо інтервал при демонтажі компонента
    }, [navigate]);

    return (
        <section className="LoadingPage">
            <div className="container">
                <div className="LoadingPage__content">
                    <div className="LoadingPage__main_content">
                        <header className="LoadingPage__header">
                            <Link className="to_load_btn" to="/">
                                <button className="back__button">
                                    Back
                                </button>
                            </Link>
                            <Link className="Logo__btn" to="/">
                                <h1 className="LoadingPage__logo">
                                    <span className="logo__purple">Web</span>Check
                                </h1>
                            </Link>
                        </header>
                        <div className="loading">
                            <h2 className="loading__description">
                                It will take some time. Please wait...
                            </h2>
                            <div className="loadingPage__main_loading">
                                <div className="progress-bar">
                                    <div className="bar"></div>
                                </div>
                            </div>
                        </div>
                        <div className="copyright">
                            <h3 className="copyright__text__dark">
                                MADE BY <span className="team_name">IPSO</span> TEAM
                            </h3>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
}

export default LoadingPage;
