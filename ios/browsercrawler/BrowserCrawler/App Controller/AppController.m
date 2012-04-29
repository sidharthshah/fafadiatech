//
//  AppController.m
//  Browser Crawler
//
//  Created by Jobin Kurian on 03/04/12.
//  Copyright (c) 2012 Fafadia Tech, Mumbai. All rights reserved.
//

#import "AppController.h"
#import "ASIHTTPRequest.h"

@implementation AppController
@synthesize tableView;
@synthesize btnStartScan;
@synthesize scanProgressBar;
@synthesize busyProgressbar;

// View loading event.
- (void)awakeFromNib {
    
    // Setting the number of history to be displayed.
    historyLimit = 10;
          
    // Progress Bar indication properties.
    [scanProgressBar setIndeterminate:NO];
    
    dataCounter = 0;
    
    // To create the app database.
    [self createAppDb];
    
    // To get all the browser's database path;
    [self getBrowserDbPath];
    
    // To get the total number of rows in chrome database. 
    [self getChromeDataCount];
    
    // To get the total number of rows in chrome database.     
    [self getFirefoxDataCount];
    
    // To get the total number of rows in safari plist.     
    [self getSafariDataCount];
}


#pragma mark - Table View Datasource

- (NSInteger)numberOfRowsInTableView:(NSTableView *)tableView {
    return [urlsArray count];
}

- (id)tableView:(NSTableView *)tableView objectValueForTableColumn:(NSTableColumn *)tableColumn row:(NSInteger)row {
    if([[tableColumn identifier]isEqualTo:@"urls"])  
        return [urlsArray objectAtIndex:row];
    else if ([[tableColumn identifier]isEqualTo:@"count"]) {
        return [visitCountArray objectAtIndex:row];
    }
    else if ([[tableColumn identifier]isEqualTo:@"ping"]) {
        return [urlsPingTime objectAtIndex:row];
    }
    else if ([[tableColumn identifier] isEqualTo:@"pageSize"]) {
        return[pageContentSize objectAtIndex:row];
    }
    return nil;
}


#pragma mark - Defined Functions

// Creating App's database to store the history from the browsers.
- (void)createAppDb {
    // Getting the users document directory.
    documentsDir = [NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES) objectAtIndex:0];
    // Getting the database path
    appDbPath = [[NSString alloc]initWithFormat:@"%@",[documentsDir stringByAppendingPathComponent:@"database.sqlite"]];
    // Check if the file exist, if true delete the database file.
    if ([[NSFileManager defaultManager] fileExistsAtPath:appDbPath]) {
        [[NSFileManager defaultManager] removeItemAtPath:appDbPath error:nil];
	}
}

// To get all the browser's database paths.
- (void)getBrowserDbPath {
    
    // Gets the Support Application Directory.
    appSupportDir = [NSSearchPathForDirectoriesInDomains(NSApplicationSupportDirectory, NSUserDomainMask, YES) objectAtIndex:0];
    appLibraryDir = [NSSearchPathForDirectoriesInDomains(NSLibraryDirectory, NSUserDomainMask, YES) objectAtIndex:0];
    
    // Chrome database name.
    chromeDBName = [NSString stringWithFormat:@"History"];
    NSString *chromeRelativePath = [NSString stringWithFormat:@"/Google/Chrome/Default/%@",chromeDBName];
    // Complete chrome database path.
    chromeDBPath = [[NSString alloc] initWithFormat:@"%@",[appSupportDir stringByAppendingPathComponent:chromeRelativePath]];
    NSLog(@"Chrome Db Path = %@",chromeDBPath);
    
    
    // Firefox database name.
    firefoxDBName = [NSString stringWithFormat:@"places.sqlite"];
    // Creating the default directories path.
    NSString *defaultFolderPath = [appSupportDir stringByAppendingPathComponent:@"/Firefox/Profiles/"];
    // Getting the default directory name since the name starts with xxxxxx.default.
    NSFileManager *fileManager = [NSFileManager defaultManager];
    NSArray *dirContents = [fileManager contentsOfDirectoryAtPath:defaultFolderPath error:nil];
    // Searching the directory for folder containing '.default'.
    NSPredicate *filter = [NSPredicate predicateWithFormat:@"self ENDSWITH '.default'"];
    NSArray *profileSubDirList = [dirContents filteredArrayUsingPredicate:filter];
    // Firefox database relative path.
    NSString *firefoxRelativePath = [defaultFolderPath stringByAppendingPathComponent:[NSString stringWithFormat:@"%@",[profileSubDirList objectAtIndex:0]]];
    // Complete firefox database path.
    firefoxDBPath = [[NSString alloc] initWithFormat:@"%@",[firefoxRelativePath stringByAppendingPathComponent:firefoxDBName]];
    NSLog(@"FireFox Db Path = %@",firefoxDBPath);
    
    
    // Safari plist name.
    safariDBName = [NSString stringWithFormat:@"History.plist"];
    NSString *safariRelativePath = [NSString stringWithFormat:@"/Safari/%@",safariDBName];
    // Complete safari plist path.
    safariDBPath = [[NSString alloc] initWithFormat:@"%@",[appLibraryDir stringByAppendingPathComponent:safariRelativePath]];
    NSLog(@"Safari Db Path = %@",safariDBPath);
    
}

// CHROME.

// To get the total number of rows in chrome database.
- (void)getChromeDataCount {
    database = [FMDatabase databaseWithPath:chromeDBPath];
    [database open];
    // Sql Query to be executed to get the id, ame, Location list based on the Dashboard category selected.
    NSString *sqlQuery = [NSString stringWithFormat:@"SELECT COUNT(*) FROM urls"];
    // Query result 
    FMResultSet *result = [database executeQuery:sqlQuery];
    while([result next]) {
        chromeDataCount = [result intForColumnIndex:0];
    }

    [database close];
    NSLog(@"Chrome Data Count = %ld",chromeDataCount);
}

// To get all the urls and visit count from chrome database.
- (void)getChromeData {
   
    database = [FMDatabase databaseWithPath:chromeDBPath];
    [database open];
    // Sql Query to be executed to get the id, ame, Location list based on the Dashboard category selected.
    NSString *sqlQuery = [NSString stringWithFormat:@"SELECT url, visit_count FROM urls"];
    // Query result 
    FMResultSet *result = [database executeQuery:sqlQuery];
    
    [scanProgressBar startAnimation:self];
    [busyProgressbar startAnimation:self];
    while([result next]) {
        // Incrementing the datacounter for progress bar.
        dataCounter++;
        
        // Getting the url and visit_count from database
        NSString *strUrl = [[NSString stringWithFormat:@"%@", [result stringForColumn:@"Url"]] stringByReplacingOccurrencesOfString:@"www." withString:@""];
        NSInteger visitCount = [result intForColumn:@"visit_count"];
        // Convert the string to an NSURL to take advantage of NSURL's parsing abilities.
        NSURL *url = [NSURL URLWithString:strUrl];
        // Get the host, e.g. "secure.twitter.com"
        NSString *host = [url host];
        
        [scanProgressBar setDoubleValue:dataCounter];
        [scanProgressBar displayIfNeeded];
        
        if (host != nil) {
            [self saveContentToAppDb:host withVisit:visitCount];
        }
    }
    [database close];
    [self getFirefoxData];
}

// FIREFOX.

// To get the total number of rows in firefox database.
- (void)getFirefoxDataCount {
    database = [FMDatabase databaseWithPath:firefoxDBPath];
    [database open];
    // Sql Query to be executed to get the id, ame, Location list based on the Dashboard category selected.
    NSString *sqlQuery = [NSString stringWithFormat:@"SELECT COUNT(*) FROM moz_places"];
    // Query result 
    FMResultSet *result = [database executeQuery:sqlQuery];
    while([result next]) {
        firefoxDataCount = [result intForColumnIndex:0];
    }
    [database close];
    NSLog(@"Firefox Data Count = %ld",firefoxDataCount);
}

// To get all the urls and visit count from firefox database.
- (void)getFirefoxData {
    
    database = [FMDatabase databaseWithPath:firefoxDBPath];
    [database open];
    // Sql Query to be executed to get the id, ame, Location list based on the Dashboard category selected.
    NSString *sqlQuery = [NSString stringWithFormat:@"SELECT url, visit_count FROM moz_places"];
    // Query result 
    FMResultSet *result = [database executeQuery:sqlQuery];
    
    [scanProgressBar startAnimation:self];
    [busyProgressbar startAnimation:self];
    while([result next]) {
        // Incrementing the datacounter for progress bar.
        dataCounter++;
        
        // Getting the url and visit_count from database
        NSString *strUrl = [[NSString stringWithFormat:@"%@", [result stringForColumn:@"Url"]] stringByReplacingOccurrencesOfString:@"www." withString:@""];
        NSInteger visitCount = [result intForColumn:@"visit_count"];
        // Convert the string to an NSURL to take advantage of NSURL's parsing abilities.
        NSURL *url = [NSURL URLWithString:strUrl];
        // Get the host, e.g. "secure.twitter.com"
        NSString *host = [url host];
        
        [scanProgressBar setDoubleValue:dataCounter];
        [scanProgressBar displayIfNeeded];
        
        if (host != nil) {
            [self saveContentToAppDb:host withVisit:visitCount];
        }
    }
    [database close];
    // Calling the function to get safari data.
    [self getSafariData];
}

// To get the total number of rows in safari plist.
- (void)getSafariDataCount {
    safariPlistContent = [[NSMutableDictionary alloc] initWithContentsOfFile:safariDBPath];
    historyArray = [[NSArray alloc] initWithArray:[safariPlistContent objectForKey:@"WebHistoryDates"]];
    safariDataCount = [historyArray count];
    NSLog(@"Safari Data Count = %ld", safariDataCount);
}

// To get all the urls and visit count from safari history plist.
- (void)getSafariData {
    
    for (NSDictionary *historyItem in historyArray) {
        // Incrementing the datacounter for progress bar.
        dataCounter++;
        // Getting the url and visit_count from the plist.
        NSString *strUrl = [[NSString stringWithFormat:@"%@", [historyItem valueForKey:@""]] stringByReplacingOccurrencesOfString:@"www." withString:@""];
        NSInteger visitCount = [[historyItem valueForKey:@"visitCount"] integerValue];
        
        // Convert the string to an NSURL to take advantage of NSURL's parsing abilities.
        NSURL *url = [NSURL URLWithString:strUrl];
        // Get the host, e.g. "secure.twitter.com"
        NSString *host = [url host];
        
        [scanProgressBar setDoubleValue:dataCounter];
        [scanProgressBar displayIfNeeded];
        
        if (host != nil) {
            [self saveContentToAppDb:host withVisit:visitCount];
        }
    }
    // Calling function to get history from the temp app database.
    [self getHistoryFromAppDb];
}

// MY APP DATABASE.

// To save the contents (url, visit_count) to the apps db.
- (void)saveContentToAppDb:(NSString *)url withVisit:(NSInteger)count {
    database = [FMDatabase databaseWithPath:appDbPath];    
    [database open];
    [database executeUpdate:@"CREATE TABLE history (urls TEXT , visit_count INT)"];
    NSString *query = [NSString stringWithFormat:@"INSERT INTO history VALUES ('%@', %ld)", url , count];
    [database executeUpdate:query];
    [database close];
}

// To get urls with visit count from the application database.
- (void)getHistoryFromAppDb {
    [scanProgressBar setMinValue:0];
    [scanProgressBar setMaxValue:historyLimit];
    [scanProgressBar setDoubleValue:0];
    [scanProgressBar displayIfNeeded];
    
    dataCounter = 0;
    
    urlsArray = [[NSMutableArray alloc] init];
    visitCountArray = [[NSMutableArray alloc] init];
    urlsPingTime = [[NSMutableArray alloc] init];
    pageContentSize = [[NSMutableArray alloc] init];
    database = [FMDatabase databaseWithPath:appDbPath];
    [database open];
    // Sql Query to be executed to get the id, Name, Location list based on the Dashboard category selected.
    NSString *sqlQuery = [NSString stringWithFormat:@"SELECT urls, sum(visit_count) AS visit_count FROM history GROUP BY urls ORDER BY visit_count DESC LIMIT %li", historyLimit];
    // Query result 
    FMResultSet *result = [database executeQuery:sqlQuery];
    while([result next]) {
        dataCounter++;
        // Getting the url from database
        NSString *visitedUrl = [result stringForColumn:@"urls"];
        NSString *visitCount = [NSString stringWithFormat:@"%d" ,[result intForColumn:@"visit_count"]];
        [urlsArray addObject:visitedUrl];
        [visitCountArray addObject:visitCount];
        [urlsPingTime addObject:[NSString stringWithFormat:@"%@",[self pingSource:visitedUrl]]];
        [pageContentSize addObject:[self contentSize:visitedUrl]];

        [scanProgressBar setDoubleValue:dataCounter];
        [scanProgressBar displayIfNeeded];
    }
    [database close];
    [busyProgressbar stopAnimation:self];
    [tableView reloadData];
    [tableView setHidden:NO];
}

// FUNCTIONALITIES.

// To ping the website and get its avg ping latency.
- (NSString *)pingSource:(NSString *)url {

    // Creating a task.
    NSTask *task = [[NSTask alloc] init];
    [task setLaunchPath:@"/sbin/ping"];
    
    // Creating the arguments to be passed to the ping.
    NSArray *arguments = [NSArray arrayWithObjects:@"-c 4", url , nil];
    [task setArguments:arguments];
    
    NSPipe *pipe = [NSPipe pipe];
    [task setStandardOutput:pipe];
    
    NSFileHandle *file = [pipe fileHandleForReading];
    
    [task launch];
    
    NSData *data = [[NSData alloc] initWithData:[file readDataToEndOfFile]];
    NSString *pingResponse = [[NSString alloc]initWithData:data encoding:NSUTF8StringEncoding];
    
    //Check if the string recieved from ping is null
    if (![pingResponse isEqualToString:@""]) {
        NSInteger lastEqualSign = [pingResponse rangeOfString:@"=" options:NSBackwardsSearch].location;
        
        NSInteger startAtIndex = lastEqualSign + 2;
        NSInteger numberOfCharacters = [pingResponse length] - startAtIndex;
        
        // String search to check if the ping to the website was fail.e
        NSRange match;
        match = [pingResponse rangeOfString: @"100.0% packet loss"];
        if (match.location == NSNotFound) {
            NSString *stringWithTime = [pingResponse substringWithRange:NSMakeRange(startAtIndex , numberOfCharacters)];
            NSArray *arrayOfTime = [stringWithTime componentsSeparatedByString: @"/"];
            NSString *pingTime = [NSString stringWithFormat:@"%@ ms",[arrayOfTime objectAtIndex:1]];
            return pingTime;
        }
        else {
            NSLog (@"Ping Failed");
            return @"NA";
        }
    }
    return @"NA";
    [pingResponse release];
    [task release];
}

// To calculate the website page content size.
- (NSString *)contentSize:(NSString *)url {
    
    ASIHTTPRequest *request = [[[ASIHTTPRequest alloc] initWithURL:[NSURL URLWithString:[NSString stringWithFormat:@"http://%@",url]]] autorelease];
	
	//Customise our user agent, for no real reason
	[request addRequestHeader:@"User-Agent" value:@"ASIHTTPRequest"];
	[request setDelegate:self];
	[request startSynchronous];
	if ([request error]) {
        NSLog(@"%@",[request error]);
        return @"NA";
	} else if ([request responseString]) {
        
        NSString *contentSize = [NSString stringWithFormat:@"%0.4f Kb",((float)[[request responseData] length])/1024];
        NSLog(@"%@",contentSize);
        return contentSize;
	}
    else {
        return @"NA";
    }
    
}


#pragma mark - UI Events
// Start scan button event.
- (IBAction)btnStartScan:(id)sender {
    
    // Progress Bar indication properties.
    [scanProgressBar setIndeterminate:NO];
    [scanProgressBar setMinValue:0];
    
    NSLog(@"%li",chromeDataCount+firefoxDataCount+safariDataCount);
    
    [scanProgressBar setMaxValue:chromeDataCount+firefoxDataCount+safariDataCount];
    
    // Setting the data counter to 0.
    dataCounter = 0;
    
    // To create the app database.
    [self createAppDb];
        
    // To get all the urls and visit count from chrome database. 
    [self getChromeData];
}



@end
