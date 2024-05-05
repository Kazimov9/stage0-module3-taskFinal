package lang.print.gaps.finalModuleTask;

public class TemperatureConverter {
    public void toFahrenheit(int temperatureCelsius){
        float fahrenheit = ((float) temperatureCelsius * 9/5) + 32;
        System.out.println(fahrenheit);
    }
}
