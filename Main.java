package com.gavin;
import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import  java.io.*;
import java.net.URL;
import java.util.*;
import java.awt.*;
import java.util.List;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;

class messages{
    public static JLabel messages=new JLabel();
}
class runtime extends Thread {
    static String serverIP = "";
    public void init(String serverIPs){
        serverIP = serverIPs;
    }

    public void run() {
        try{
            System.out.println ("Thread " +Thread.currentThread().getId() + " is running");
            String Data = "";

            while(true){

                if(true){
                    Process p = Runtime.getRuntime().exec("client.exe -getData "+serverIP);

                    BufferedReader procInput = new BufferedReader(new
                            InputStreamReader(p.getInputStream()));
                    Data = procInput.readLine();
                }
                messages.messages.setText("<html>"+Data.replaceAll("%G2%12%99","<br/>")+"</html>");

            }
        }
        catch (Exception e){
            e.printStackTrace();
        }
    }
}

public class Main {

    static boolean connectedToServer = false;
    static String serverIP = "";

    public static void joinRoomWindow(){
        JFrame frame = new JFrame("LanChat Join Room");
        frame.setResizable(false);
        frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        frame.setBounds(0, 0, 300, 160);
        frame.setLayout(null);
        frame.getContentPane().setBackground(new Color(18, 22, 49));

        JTextField input = new JTextField("input url",16);
        input.setBounds(0,0,150,25);

        JButton join = new JButton("join");
        join.setBounds(0,50,140,25);

        join.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                connectedToServer = true;
                serverIP = "http://"+input.getText();
                frame.setVisible(false);
                runtime thread = new runtime();
                thread.init(serverIP);
                thread.start();
            }
        });

        frame.add(join);
        frame.add(input);
        frame.setVisible(true);
    }
    public static void main(String[] args) throws IOException, InterruptedException {
        JFrame frame = new JFrame("LanChat");
        frame.setResizable(false);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setBounds(0, 0, 500, 400);
        frame.setLayout(null);
        frame.getContentPane().setBackground(new Color(18, 22, 49));

        JPanel panel=new JPanel();
        panel.setBounds(40,30,445,290);
        panel.setBackground(new Color(26, 46, 84));




        messages.messages.setBounds(panel.getBounds());

        messages.messages.setFont(new Font("Arial",Font.PLAIN,20));
        messages.messages.setForeground(new Color(0, 214, 255));

        JTextField input = new JTextField("input message",16);
        input.setBounds(70,330,410,25);

        JButton join = new JButton("join server");
        join.setBounds(frame.getBounds().width/2-25,0,100,25);

        JButton Send = new JButton("send");
        Send.setBounds(5,330,65,25);

        Send.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    sendData(input.getText());
                } catch (IOException ex) {
                    ex.printStackTrace();
                }
            }
        });

        join.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                joinRoomWindow();
            }
        });
        frame.add(Send);
        frame.add(messages.messages);
        frame.add(input);
        frame.add(panel);
        frame.add(join);

        frame.setVisible(true);

    }

    public static void sendData(String Data) throws IOException {
        if(connectedToServer){
            Process p = Runtime.getRuntime().exec("client.exe -sendData "+serverIP+" "+Data.replaceAll(" ","%E2%96%88"));


        }
    }
}
