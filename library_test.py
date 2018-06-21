import unittest
import library

NUM_CORPUS = '''
On the 5th of May every year, Mexicans celebrate Cinco de Mayo. This tradition
began in 1845 (the twenty-second anniversary of the Mexican Revolution), and
is the 1st example of a national independence holiday becoming popular in the
Western Hemisphere. (The Fourth of July didn't see regular celebration in the
US until 15-20 years later.) It is celebrated by 77.9% of the population--
trending toward 80.                                                                
'''

class TestCase(unittest.TestCase):

    # Helper function
    def assert_extract(self, text, extractors, *expected):
        actual = [x[1].group(0) for x in library.scan(text, extractors)]
        self.assertEquals(str(actual), str([x for x in expected]))

    # First unit test; prove that if we scan NUM_CORPUS looking for mixed_ordinals,
    # we find "5th" and "1st".
    def test_mixed_ordinals(self):
        self.assert_extract(NUM_CORPUS, library.mixed_ordinals, '5th', '1st')

    # Second unit test; prove that if we look for integers, we find four of them.
    def test_integers(self):
        self.assert_extract(NUM_CORPUS, library.integers, '1845', '15', '20', '80')

    # Third unit test; prove that if we look for integers where there are none, we get no results.
    def test_no_integers(self):
        self.assert_extract("no integers", library.integers)

    # Fourth unit test; 
    def test_dates(self):
        self.assert_extract("I was born on 2015-07-25.", library.dates_iso8601, '2015-07-25')
    
    # Fifth unit test; 
    def test_wrong_date(self):
        self.assert_extract("is this date correct 2015-13-25.", library.dates_iso8601)

    # Sixth unit test; 
    def test_human_dates(self):
        self.assert_extract("I was born on 25 Jan 2017.", library.dates_human, '25 Jan 2017')

    # failing tests
    def match_complex_dates(self):
        ''' dates with time stamps with minute '''
        self.assert_extract("I was born on 2008-09-15T15:53.", library.complex_date_time, '2008-09-15T15:53')

        ''' dates with time stamp with seconds'''
        self.assert_extract("I was born on 2008-09-15T15:53:00.", library.complex_date_time, '2008-09-15T15:53:00')

        ''' dates with time stamp with milliseconds '''
        self.assert_extract("I was born on 2008-09-15T15:53:00.322345.", library.complex_date_time, '2008-09-15T15:53:00.322345')

        ''' date time seperated with space '''
        self.assert_extract("I was born on 2008-09-15 15:53:00.", library.complex_date_time, '2008-09-15 15:53:00')

        ''' date time seperated with T '''
        self.assert_extract("I was born on 2008-09-15T15:53:00.", library.complex_date_time, '2008-09-15T15:53:00')

        ''' with three letter Timezone '''
        self.assert_extract("I was born on 2008-09-15T15:53:00 EST.", library.complex_date_time, '2008-09-15T15:53:00 ES')

        ''' with one letter Timezone '''
        self.assert_extract("I was born on 2008-09-15T15:53:00Z.", library.complex_date_time, '2008-09-15T15:53:00Z')

        ''' with Time offset '''
        self.assert_extract("I was born on 2008-09-15T15:53:00 -0800.", library.complex_date_time, '2008-09-15T15:53:00 -0800')

        ''' with time stamp with milliseconds and Time offset and space'''
        self.assert_extract("I was born on 2008-09-15 15:53:00.345623 -0800.", library.complex_date_time, '2008-09-15 15:53:00.345623 -0800')

        ''' with time stamp with seconds and three letter Timezone and T'''
        self.assert_extract("I was born on 2008-09-15T15:53:00 EST.", library.complex_date_time, '2008-09-15T15:53:00 EST')
    
    def match_grouped_numbers(self):
        self.assert_extract("pay me 123,456,789.", library.grouped_number, '123,456,789')
        self.assert_extract("pay me 12,34,56,789.", library.grouped_number, '12,34,56,789')




if __name__ == '__main__':
    unittest.main()
