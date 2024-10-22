import { useState } from 'react';
import QrReader from 'react-qr-reader';

function QRScanner({ onScanComplete }) {
    const [error, setError] = useState(null);

    const handleScan = (data) => {
        if (data) {
            onScanComplete(data); // process the scanned data
        }
    };

    const handleError = (err) => {
        setError(err);
    };

    return (
        <div>
            {error && <p>Error: {error}</p>}
            <QrReader
                delay={300}
                onError={handleError}
                onScan={handleScan}
                style={{ width: '100%' }}
            />
        </div>
    );
}

export default QRScanner;