package com.company;
import com.sun.javafx.image.impl.IntArgb;

import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import  java.io.*;
import java.net.URL;
import java.nio.file.Paths;
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
                try{
                    messages.messages.setText("<html>"+Data.replace("%Eg%v7%8","<br>")+"</html>");
                }
                catch (Exception e){
                    messages.messages.setText("<html>"+Data+"</html>");
                }



            }
        }
        catch (Exception e){
            e.printStackTrace();
        }
    }
}

class sendThread extends Thread{
    String serverIP = "";
    String Data = "";
    public void init(String _serverIP,String _Data){
         serverIP= _serverIP;
         Data = _Data;
    }
    public void run(){
        try {
            Process p = Runtime.getRuntime().exec("client.exe -sendData "+serverIP+" "+Data.replaceAll(" ","%E2%96%88"));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

public class Main {
    static JButton Send = new JButton("send");
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
                serverIP = input.getText();
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




        messages.messages.setBounds(40,30,445,290);

        messages.messages.setFont(new Font("Arial",Font.PLAIN,20));
        messages.messages.setForeground(new Color(0, 214, 255));


        JTextField input = new JTextField("input message",16);
        input.setBounds(70,330,410,25);

        JButton join = new JButton("join server");
        join.setBounds(frame.getBounds().width/2-25,0,100,25);

        JButton startServer = new JButton("start server");
        startServer.setBounds(0,0,110,25);


        Send.setBounds(5,330,65,25);

        Send.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    sendData(input.getText());
                } catch (IOException ioException) {
                    ioException.printStackTrace();
                }
            }
        });

        startServer.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                String data = "";
                try {
                    Process p = Runtime.getRuntime().exec("client.exe -findServIp");
                    p.waitFor();
                    JFrame frame2 = new JFrame("LanChat Start Server");
                    frame2.setResizable(false);
                    frame2.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
                    frame2.setBounds(0, 0, 300, 300);
                    frame2.setLayout(null);
                    frame2.getContentPane().setBackground(new Color(18, 22, 49));


                    JButton start = new JButton("start server");
                    start.setBounds(30,0,120,25);

                    BufferedReader procInput = new BufferedReader(new
                            InputStreamReader(p.getInputStream()));
                    data =  procInput.readLine();

                    System.out.println(data);

                    JLabel dataText=new JLabel();
                    dataText.setText("<html>after pressing 'start server' put: <u><b>"+data+"</b></u> :as the ip/url to enter server</html>");
                    dataText.setBounds(0,30,300,75);
                    dataText.setForeground(new Color(0, 255, 238));
                    dataText.setFont(new Font("Arial",Font.PLAIN,20));

                    String finalData = data;
                    start.addActionListener(new ActionListener() {
                        public void actionPerformed(ActionEvent e) {
                            try {
                                Process p = Runtime.getRuntime().exec("cmd.exe /c start client.exe -startServ "+finalData.replaceAll(":"," "));
                                frame2.dispose();
                                serverIP = finalData;
                                runtime thread = new runtime();
                                thread.init(serverIP);
                                thread.start();
                                connectedToServer = true;
                            } catch (IOException ex) {
                                ex.printStackTrace();
                            }
                        }
                    });

                    frame2.add(start);
                    frame2.add(dataText);
                    frame2.setVisible(true);
                } catch (IOException | InterruptedException ex) {
                    ex.printStackTrace();
                }
            }
        });

        join.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                joinRoomWindow();
            }
        });
        frame.add(startServer);
        frame.add(Send);
        frame.add(messages.messages);
        frame.add(input);
        frame.add(panel);
        frame.add(join);

        frame.setVisible(true);

    }

    public static void sendData(String Data) throws IOException {
        if(connectedToServer){
            sendThread thread = new sendThread();
            thread.init(serverIP,Data);
            thread.start();
        }
    }
}

