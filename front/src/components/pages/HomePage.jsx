import React, { useState } from 'react';
import axios from 'axios';
import '../styles/StyleHomePage.scss';
import { Link } from 'react-router-dom';

function HomePage() {
    // Declare state variables using useState
    const [url, setUrl] = useState("");        // URL input by user
    const [results, setResults] = useState(null); // Store scan results
    const [loading, setLoading] = useState(false); // For loading state (while scanning)
    const [error, setError] = useState(null);   // Store error messages (if any)

    // Start scanning when the user clicks the "Submit" button
    const startScan = async () => {
        
        if (url.trim() === '') return;

        console.log('work')
        setLoading(true);  // Set loading to true when scan starts
        setError(null);    // Clear any previous errors
        setResults(null);  // Clear any previous results

        try {
            console.log("URL to scan:", url); // Log URL for debugging

            // Send the URL entered by the user to the Flask backend
            const response = await axios.post("http://127.0.0.1:5000/start-scan", { url });

            // Check if the response is successful
            if (response.data.status === "success") {
                setResults(response.data.results);  // Set the scan results in state
            } else {
                setError("Scan failed. Please try again.");  // Handle scan failure
            }

        } catch (err) {
            // Handle error gracefully
            console.error("Error occurred during scan:", err); // Log the error for debugging
            setError(err.response?.data?.message || "An error occurred during the scan.");
        } finally {
            setLoading(false);  // Set loading to false once scan is complete
        }
    };

    return (


        <section className="HomePage">
            <div className="container">
                <div className="HomePage__content">
                    <div className="HomePage__main_content">
                        <div className="HomePage__title">
                            <h1 className='HomePage__logo'>
                                <span className='logo__puprle'>Web</span>Check
                            </h1>
                            <h2 className='HomePage__subTitle'>Check security of your website</h2>
                        </div>
                        <div className="HomePage__function">
                            <input
                                value={url}
                                onChange={(e) => setUrl(e.target.value)} // Update state when user types in input
                                className='function__input'
                                type="text"
                                name="url_link"
                                id="url_link"
                                placeholder='Enter your URL'
                            />
                            <Link className='to_load_btn' to="/loading">
                                <button onClick={startScan} className="function__button">
                                    {loading ? "Scanning..." : "SUBMIT"} {/* Show loading text when scanning */}
                                </button>
                            </Link>
                        </div>
                        <div className="copyright">
                            <h3 className='copyright__text'>
                                MADE BY <span className='team_name'>IPSO</span> TEAM
                            </h3>
                        </div>

                        {/* Display the results or error message */}
                        {results && (
                            <div>
                                <h2>Scan Results</h2>
                                <pre>{JSON.stringify(results, null, 2)}</pre>
                            </div>
                        )}

                        {error && (
                            <div style={{ color: 'red' }}>
                                <h3>Error: {error}</h3>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </section>
    );
}

export default HomePage;
