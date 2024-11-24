import React from 'react';
import '../styles/StyleHomePage.scss';

function HomePage() {


    return (
        <section className="HomePage">
            {/* <div className='top__blur'></div> */}
            <div className="container">
                <div className="HomePage__content">
                    <div className="HomePage__main_content">
                        <div className="HomePage__title">
                            <h1 className='HomePage__logo'><span className='logo__puprle'>Web</span>Check</h1>
                            <h2 className='HomePage__subTitle'>Check security of your website</h2>
                        </div>
                        <div className="HomePage__function">
                            <input className='function__input' type="text" name="url_link" id="url_link" placeholder='Enter your URL or localhost' />
                            <button className="function__button">SUBMIT</button>
                        </div>
                        <div className="copyright"><h3 className='copyright__text'>MADE BY <span className='team_name'>IPSO</span> TEAM</h3></div>
                    </div>
                </div>
            </div>
        </section>
    )


}

export default HomePage;
