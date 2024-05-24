// src/calculation.specs.js

describe('fetchDataAndCalculate', function() {
    it('should calculate average and standard deviation', function() {
        const data = [
            { 'test': 80 },
            { 'test': 90 },
            { 'test': 100 }
        ];
        const result = fetchDataAndCalculate(data, 'test');
        expect(result).toEqual({ avg: '90.00', stdDev: '8.16' });
    });
});

describe('calculateNormalizedScores', function() {
    it('should calculate normalized score', function() {
        const avg = 90;
        const outof = 100;
        const result = calculateNormalizedScores(avg, outof);
        expect(result).toBe('0.90');
    });

    it('should throw an error for invalid values', function() {
        expect(function() {
            calculateNormalizedScores(NaN, 100);
        }).toThrowError('Invalid values for normalization');
    });
});

describe('calculateNormalizedStd', function() {
    it('should calculate normalized standard deviation', function() {
        const avg = 90;
        const std = 8.16;
        const result = calculateNormalizedStd(avg, std);
        expect(result).toBe('0.09');
    });

    it('should throw an error for invalid values', function() {
        expect(function() {
            calculateNormalizedStd(NaN, 8.16);
        }).toThrowError('Invalid values for normalization');
    });
});
