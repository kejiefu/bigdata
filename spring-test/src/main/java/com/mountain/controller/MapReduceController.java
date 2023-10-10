package com.mountain.controller;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.util.ToolRunner;
import org.springframework.web.bind.annotation.RequestMapping;

import java.io.IOException;

/**
 * @author: kejiefu
 * @create: 2023-10-10 11:35
 **/
public class MapReduceController {

    @RequestMapping("/test2")
    public void test() throws Exception {
        Configuration configuration = new Configuration();
        configuration.set("hello","world");
        //提交run方法之后，得到一个程序的退出状态码
        int run = ToolRunner.run(configuration, new WordCount(), null);
        //根据我们 程序的退出状态码，退出整个进程
        System.exit(run);
    }

}
