import React from 'react';
import '../styles/StyleLoadingPage.scss';

function LoadingPage() {


    return (
        <section className="LoadingPage">
            <div className="container">
                <div className="LoadingPage__content">
                    <div className="LoadingPage__main_content">
                    <header className="LoadingPage__header">
                        <button className="back__button">
                            Back
                        </button>
                        <h1 className='LoadingPage__logo'><span className='logo__purple'>Web</span>Check</h1>
                    </header>
                    <div className="loading">
                        <h2 className="loading__description">
                            It will take some time. Please wait...
                        </h2>
                        <div className="loadingPage__main_loading"></div>
                    </div>
                    <div className="copyright"><h3 className='copyright__text__dark'>MADE BY <span className='team_name'>IPSO</span> TEAM</h3></div>
                    </div>
                </div>
            </div>
        </section>
    )


}

export default LoadingPage;
