
struct luminance
{
    uint16_t r1;
    uint16_t r2;
};


void setup()
{
    Serial.begin(9600);
}

/*
    1023 - разрыв цепи, абсолютно сухой грунт
    ~350-400 если окунуть в воду
*/
int get_soil()
{
    int a0 = analogRead(A0);

    if (a0 < 350)
        a0 = 350;
    
    // переворачиваем диапазон. 0 - сухая почва
    a0 = map(a0, 350, 1023, 100, 0);
    return a0;
}


/*
    
*/
void get_luminance( luminance& lum )
{
    lum.r1 = analogRead(A1);
    lum.r2 = analogRead(A2);

    return;
}


void loop()
{
    
    luminance lum;

    Serial.print("Soil: ");
    Serial.println( get_soil() );

    Serial.print("Lum: ");
    get_luminance(lum);
    Serial.print(lum.r1);
    Serial.print(" ");
    Serial.println(lum.r2);

    delay(2000);
    return;
}