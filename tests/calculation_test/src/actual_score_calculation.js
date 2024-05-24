// tests/calculation_test/src/actual_score_calculation.js

function calculateActualScore(piValues, piWeights) {
    let sum = 0;

    piValues.forEach(function(pi) {
        let piWeightResult = piWeights.piAverageSuccess[pi] || 0.00;
        sum += piWeightResult;
    });

    const averagePI = sum / piValues.length;
    return (averagePI * 5).toFixed(2);
}

// Export function for testing if in Node.js environment
if (typeof module !== 'undefined' && module.exports) {
    module.exports = calculateActualScore;
}
