// tests/calculation_test/src/actual_score_calculation.spec.js

describe('calculateActualScore', function() {
    it('should calculate the actual score correctly', function() {
        const piValues = ['PI-c1', 'PI-b2', 'PI-c5'];
        const piWeights = {
            piAverageSuccess: {
                'PI-c1': 0.6,
                'PI-b2': 0.8,
                'PI-c5': 0.9
            }
        };

        const actualScore = calculateActualScore(piValues, piWeights);
        expect(actualScore).toBe('3.83'); // ((0.6 + 0.8 + 0.9) / 3) * 5
    });

    it('should handle missing PI values gracefully', function() {
        const piValues = ['PI-c1', 'PI-c6', 'PI-c5'];
        const piWeights = {
            piAverageSuccess: {
                'PI-c1': 0.6,
                'PI-c5': 0.9
            }
        };

        const actualScore = calculateActualScore(piValues, piWeights);
        expect(actualScore).toBe('2.50'); // ((0.6 + 0 + 0.9) / 3) * 5
    });
});
