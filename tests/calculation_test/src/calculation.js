// tests/calculation_test/src/calculation.js

function fetchDataAndCalculate(data, checkboxValue) {
    let total = 0;
    let squaredDifferencesSum = 0;

    data.forEach(function (student) {
        let value = student[checkboxValue];
        total += value;
    });

    const avg = (total / data.length).toFixed(2);

    data.forEach(function (student) {
        let value = student[checkboxValue];
        squaredDifferencesSum += Math.pow(value - avg, 2);
    });

    const stdDev = Math.sqrt(squaredDifferencesSum / data.length).toFixed(2);

    return { avg, stdDev };
}

function calculateNormalizedScores(avg, outof) {
    if (!isNaN(avg) && !isNaN(outof) && outof !== 0) {
        return (avg / outof).toFixed(2);
    } else {
        throw new Error('Invalid values for normalization');
    }
}

function calculateNormalizedStd(avg, std) {
    if (!isNaN(avg) && !isNaN(std) && std !== 0) {
        return (std / avg).toFixed(2);
    } else {
        throw new Error('Invalid values for normalization');
    }
}

// Export functions for testing if in Node.js environment
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        fetchDataAndCalculate,
        calculateNormalizedScores,
        calculateNormalizedStd
    };
}
