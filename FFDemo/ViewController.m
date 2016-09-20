//
//  ViewController.m
//  FFDemo
//
//  Created by yujinyu on 16/6/23.
//  Copyright © 2016年 yujinyu. All rights reserved.
//

#import "ViewController.h"

@interface ViewController ()

- (void)initNavBar;

@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view, typically from a nib.
    [self initNavBar];

}

- (void)viewWillAppear:(BOOL)animated
{
    NSLog(@"view will appear ");
    
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}


#pragma mark -- custom methods

- (void)initNavBar
{
    self.navigationItem.title = @"Firefly";
    
    self.view.backgroundColor = [UIColor whiteColor];

}


@end
