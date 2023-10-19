package com.mountain.controller;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataOutputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.security.UserGroupInformation;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.io.IOException;

/**
 * @author: kejiefu
 * @create: 2023-10-10 11:01
 **/
@RestController
public class HDFSWriteTest2Controller {

    @RequestMapping("/test2")
    public void test() throws IOException {
        try {
            Configuration conf = new Configuration();
            conf.set("fs.defaultFS", "hdfs://192.168.110.26:9000");

            FileSystem fs = FileSystem.get(conf);

            // 指定要写入的文件路径
            Path filePath = new Path("/user/hadoop/example.txt");

            // 创建文件写入流
            FSDataOutputStream outputStream = fs.create(filePath);

            // 写入数据
            String data = "Hello, HDFS!";
            outputStream.write(data.getBytes());

            // 关闭流
            outputStream.close();

            System.out.println("File written successfully.");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    //本地可以执行
    public static void main(String[] args) {
        try {
            // 设置Hadoop配置
            Configuration conf = new Configuration();
            conf.set("fs.defaultFS", "hdfs://192.168.110.26:9000");

            // 设置要使用的用户
            String userName = "hadoop";
            UserGroupInformation ugi = UserGroupInformation.createRemoteUser(userName);

            // 在特权模式下执行HDFS操作
            ugi.doAs((java.security.PrivilegedExceptionAction<Void>) () -> {
                try {
                    // 获取文件系统
                    FileSystem fs = FileSystem.get(conf);

                    // 指定要写入的文件路径
                    Path filePath = new Path("/user/hadoop/example.txt");

                    // 创建文件写入流
                    FSDataOutputStream outputStream = fs.create(filePath);

                    // 写入数据
                    String data = "Hello, HDFS!";
                    outputStream.write(data.getBytes());

                    // 关闭流
                    outputStream.close();

                    System.out.println("Data written to HDFS successfully.");
                } catch (Exception e) {
                    e.printStackTrace();
                }
                return null;
            });
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

}
