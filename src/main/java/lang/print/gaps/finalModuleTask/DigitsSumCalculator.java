package lang.print.gaps.finalModuleTask;

public class DigitsSumCalculator {
    public void calculateSum(int number) {
        int n,sum = 0;
        while (number > 0) {
            n = number % 10;
            sum = sum + n;
            number = number/10;
        }
        System.out.println(sum);
    }
}
