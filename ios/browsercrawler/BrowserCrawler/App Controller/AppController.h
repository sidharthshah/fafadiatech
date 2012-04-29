//
//  AppController.h
//  Browser Crawler
//
//  Created by Jobin Kurian on 03/04/12.
//  Copyright (c) 2012 Fafadia Tech, Mumbai. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "FMDatabase.h"
#import "FMDatabaseAdditions.h"

@interface AppController : NSObject {
    
    NSString *appSupportDir;
    NSString *appLibraryDir;
    FMDatabase *database;
    
    // App Db
    NSString *documentsDir;
    NSString *appDbPath;
    
    // Chrome
    NSString *chromeDBPath;
    NSString *chromeDBName;
    NSInteger chromeDataCount;
    
    NSInteger dataCounter;
    NSInteger historyLimit;
    
    // Firefox
    NSString *firefoxDBPath;
    NSString *firefoxDBName;
    NSInteger firefoxDataCount;
    
    // Safari
    NSString *safariDBPath;
    NSString *safariDBName;
    NSInteger safariDataCount;
    
    NSMutableDictionary *safariPlistContent;
    NSArray *historyArray;
    
    NSMutableArray *urlsArray, *visitCountArray, *urlsPingTime, *pageContentSize;
}

@property (assign) IBOutlet NSTableView *tableView;
@property (assign) IBOutlet NSButton *btnStartScan;
@property (assign) IBOutlet NSProgressIndicator *scanProgressBar;
@property (assign) IBOutlet NSProgressIndicator *busyProgressbar;


#pragma mark - UI Events
- (IBAction)btnStartScan:(id)sender;


#pragma mark - Defined Functions

// Creating App's database to store the history from the browsers.
- (void)createAppDb;

// To get all the browser's database paths.
- (void)getBrowserDbPath;

// To get the total number of rows in chrome database.
- (void)getChromeDataCount;

// To get all the urls and visit count from chrome database.
- (void)getChromeData;

// To get the total number of rows in firefox database.
- (void)getFirefoxDataCount;

// To get all the urls and visit count from firefox database.
- (void)getFirefoxData;

// To get the total number of rows in safari plist.
- (void)getSafariDataCount;

// To get all the urls and visit count from safari history plist.
- (void)getSafariData;

// To save the contents (url, visit_count) to the apps db.
- (void)saveContentToAppDb:(NSString *)url withVisit:(NSInteger)count;

// To get urls with visit count from the application database.
- (void)getHistoryFromAppDb;

// To ping the website and get its avg ping latency.
- (NSString *)pingSource:(NSString *)url;

// To calculate the website page content size.
- (NSString *)contentSize:(NSString *)url;

@end
