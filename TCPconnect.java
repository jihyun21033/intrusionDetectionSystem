import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.Date;
import java.util.Map;
import java.io.FileReader;

import com.kt.smcp.gw.ca.comm.exception.SdkException;
import com.kt.smcp.gw.ca.gwfrwk.adap.stdsys.sdk.tcp.BaseInfo;
import com.kt.smcp.gw.ca.gwfrwk.adap.stdsys.sdk.tcp.IMCallback;
import com.kt.smcp.gw.ca.gwfrwk.adap.stdsys.sdk.tcp.IMTcpConnector;
import com.kt.smcp.gw.ca.util.IMUtil;
import com.pi4j.io.gpio.GpioController;
import com.pi4j.io.gpio.GpioFactory;
import com.pi4j.io.gpio.GpioPinDigitalOutput;
import com.pi4j.io.gpio.PinState;
import com.pi4j.io.gpio.RaspiPin;
import com.pi4j.io.gpio.GpioPin;
import com.pi4j.io.gpio.GpioPinDigitalInput;
import com.pi4j.io.gpio.PinPullResistance;

public class TCPconnect extends IMCallback
{
    private GpioController gpio = null;
    private GpioPinDigitalOutput pin1 = null;
    private static GpioPinDigitalInput pin2 = null;
    private static Double pirSensor=0.0;
    private static Double sound=0.0;
    private static Double attackHome=0.0;
    private static String userName = "default";

    private static String[] arStr=null;

    public TCPconnect()
    {
        gpio = GpioFactory.getInstance();
        pin1 = gpio.provisionDigitalOutputPin(RaspiPin.GPIO_07, "PinPIR", PinState.HIGH);
        pin2 = gpio.provisionDigitalInputPin(RaspiPin.GPIO_04,"PinTC", PinPullResistance.PULL_DOWN);
    }

    public static void main(String[] args) throws Exception
    {
        raspberry callback = new raspberry();
        IMTcpConnector tcpConnector = new IMTcpConnector(); //TCP 커넥팅 모듈
        BaseInfo baseInfo = null; // 같음

        Long transID;
        Long timeOut = (long)3000; 

        try
        {
            baseInfo = IMUtil.getBaseInfo("IoTSDK.properties"); 
            tcpConnector.init(callback, baseInfo);

            tcpConnector.connect(timeOut);
            tcpConnector.authenticate(timeOut);

            while(true)
            {
                transID = IMUtil.getTransactionLongRoundKey4(); 
                getValue();
                tcpConnector.requestNumColecData("pirSensor", pirSensor, new Date(), transID); 
                tcpConnector.requestNumColecData("sound",sound, new Date(), transID);
                tcpConnector.requestNumColecData("home",attackHome, new Date(), transID);
                tcpConnector.requestStrColecData("userName", userName, new Date(), transID);
                Thread.sleep(1500);
            }

        } catch(SdkException e) 
        {
            System.out.println("Code :" + e.getCode() + " Message :" + e.getMessage());
        }
    }

     private static void getValue() throws Exception
    {
        Runtime run = Runtime.getRuntime();
        Process proc= run.exec("sudo python3 MainSensor.py");
        BufferedReader stdInput = new BufferedReader(new FileReader("data.txt"));
        String s = null;
        while((s = stdInput.readLine()) != null) 
        {
            arStr=s.split("\\s");
            pirSensor = Double.parseDouble(arStr[1]);
            sound = Double.parseDouble(arStr[2]);
            attackHome = Double.parseDouble(arStr[0]);
            userName = arStr[3];
        }        
       
    }

    @Override
    public void handleColecRes(Long transId, String respCd)
    {
        System.out.println("Collect Response. Transaction ID :" + transId + " Response Code : " + respCd);
    }

    @Override
    public void handleControlReq(Long transID, Map<String, Double> numberRows, Map<String, String> stringRows)
    {
        System.out.println("Handle Control Request Called. Transaction ID : " + transID);
        System.out.println(numberRows.size()+" Number Type controls. " + stringRows.size() + " String Type controls.");
    }
}
