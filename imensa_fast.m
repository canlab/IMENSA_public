function wgdata = imensa_fast()


%% default setting
testmode = false;
practice_repeat = 10;
response_repeat = 30;
SID =    input('  [IMENSA]  SubjectID?  number only         >> ');
SessID = input('  [IMENSA]  Visit?      1:First, 2:Second   >> ');

wgdata.subject = sprintf('sub%03d', SID);
wgdata.visit = SessID;
wgdata.start_time= datestr(clock, 0);

basedir = 'C:\Users\Dartmouth College\Dropbox (Dartmouth College)\Dartmouth\research\IMENSA_project\experiment\scripts\imensa';
subdir = fullfile(basedir, 'fast_data', wgdata.subject, sprintf('sess%d', SessID));
wgdata.wordfile = fullfile(subdir, sprintf('imensa_%s_sess%d_fast.mat', wgdata.subject, SessID));

if ~exist(subdir, 'dir')
    mkdir(subdir)
end

cd(fullfile(basedir,'fast_data'))






practice_seed = {'Dartmouth','College'};
seed_set = {'Tear drop', 'Mirror', 'Fall', 'Family', 'Chicken', 'Knife', 'Eggs', 'Rain', 'Earthquake', 'Politician', 'Pain', 'Happiness';
    'Crying', 'Reflection', 'Spring', 'Friends', 'Cow', 'Axe', 'Milk', 'Sun', 'Hurricane', 'Government', 'Suffering', 'Well-being'};
rng('shuffle');
seed = seed_set(SessID,randperm(size(seed_set,2)));
wgdata.seed = seed;
xlsx_name = fullfile(subdir, sprintf('imensa_%s_sess%d_fast.xlsx', wgdata.subject, SessID));
writetable(table(seed), xlsx_name)
save(wgdata.wordfile, 'wgdata');


%% SETUP: Screen
global theWindow W H; % window property
global white red orange bgcolor; % color
global window_rect; % rating scale

bgcolor = 100;
white = 255;
red = [158 1 66];
orange = [255 164 0];
screens = Screen('Screens');
window_num = screens(end);
Screen('Preference', 'SkipSyncTests', 0);
window_info = Screen('Resolution', window_num);

if testmode
    window_rect = [0 0 1280 800]; % in the test mode, use a little smaller screen
else   
    window_rect = [0 0 1980 1080]; % in the test mode, use a little smaller screen
    %     window_rect = [0 0 window_info.width window_info.height]; %0 0 1920 1080
end

W = window_rect(3); % width of screen
H = window_rect(4); % height of screen
textH = H/2.3;
fontsize = 40;

%% START: Screen
theWindow = Screen('OpenWindow', window_num, bgcolor, window_rect); % start the screen
% Screen('Preference','TextEncodingLocale','ko_KR.UTF-8');
% Screen('TextFont', theWindow, font);
Screen('TextSize', theWindow, fontsize);
% HideCursor;


%% TAST START: ===========================================================

try
    %% PROMPT SETUP:
    intro_prompt{1} = double('Free association task');
    intro_prompt{2} = double('');
    intro_prompt{3} = double('An orange-colored seed word will appear on screen for 4 seconds.');
    intro_prompt{4} = double('At the beep/fixation cross, state any word that comes to mind.');
    intro_prompt{5} = double('You will say one new word about every 2 seconds, until you have said 30 words per seed word.');
    intro_prompt{6} = double('Press space when you are ready to start the practice trial.');
    
    practice_start{1} = double('For the practice trial, you will be given 1 association.');
    practice_start{2} = double('Press "s" when you are ready to start.');
    
    run_start{1} = double('You have completed this run. A new run with a new seed word will start.');
    run_start{2} = double('At each beep/fixation cross, say a word that comes to mind.');
    run_start{3} = double('Press "s" when you are ready to start.');
    
    run_end_prompt = double('The free association task has ended. Thank you.');
    
    %% DISPLAY EXP START MESSAGE
    while (1)
        [~,~,keyCode] = KbCheck;
        if keyCode(KbName('space'))==1
            break
        elseif keyCode(KbName('q'))==1
            abort_man;
        end
        Screen(theWindow,'FillRect',bgcolor, window_rect);
        for i = 1:numel(intro_prompt)
            DrawFormattedText(theWindow, intro_prompt{i}, 'center', textH-50*(3-i), white);
        end
        Screen('Flip', theWindow);
    end
    
    waitsec_fromstarttime(GetSecs, .3);
    
    % 3 seconds: Blank
    Screen(theWindow,'FillRect',bgcolor, window_rect);
    Screen('Flip', theWindow);
    
    waitsec_fromstarttime(GetSecs, 3);
    
    %% MAIN PART of the experiment
    
    Screen(theWindow, 'FillRect', bgcolor, window_rect);
    DrawFormattedText(theWindow, '+','center', textH, white);
    Screen('Flip', theWindow);
    waitsec_fromstarttime(GetSecs, 3);
    
    time_fromstart = 4:2:2*(response_repeat+1);
    
    % practice
    while (1)
        [~,~,keyCode] = KbCheck;
        if keyCode(KbName('s'))==1
            break
        elseif keyCode(KbName('q'))==1
            abort_man;
        end
        Screen(theWindow,'FillRect',bgcolor, window_rect);
        for i = 1:numel(practice_start)
            DrawFormattedText(theWindow, practice_start{i},'center', textH-50*(2-i), white);
        end
        Screen('Flip', theWindow);
    end
    practice_time = GetSecs; % seed word timestamp
    for response_n = 1:practice_repeat
        % seed word for 2s
        if response_n == 1
            Screen('FillRect', theWindow, bgcolor, window_rect);
            Screen('TextSize', theWindow, fontsize*2); % emphasize
            DrawFormattedText(theWindow, double(practice_seed{SessID}),'center', textH, orange);
            Screen('Flip', theWindow);
            waitsec_fromstarttime(practice_time, 2);
        end
        
        Screen('FillRect', theWindow, bgcolor, window_rect);
        Screen('Flip', theWindow);
        
        % beeping
        beep = MakeBeep(1000,.2);
        Snd('Play',beep);
        
        % cross for 1s
        Screen('FillRect', theWindow, bgcolor, window_rect);
        Screen('TextSize', theWindow, fontsize*1.2); % emphasize
        DrawFormattedText(theWindow, '+', 'center', textH, white);
        Screen('Flip', theWindow);
        waitsec_fromstarttime(practice_time, time_fromstart(response_n)-1)
        
        % blank for 1.5s
        Screen('FillRect', theWindow, bgcolor, window_rect);
        Screen('Flip', theWindow);
        waitsec_fromstarttime(practice_time, time_fromstart(response_n))
    end
    
    
    
    % main run
    for run_i = 1:size(seed_set,2)
        while (1)
            [~,~,keyCode] = KbCheck;
            if keyCode(KbName('s'))==1
                break
            elseif keyCode(KbName('q'))==1
                abort_man;
            end
            Screen(theWindow,'FillRect',bgcolor, window_rect);
            for i = 1:numel(run_start)
                DrawFormattedText(theWindow, run_start{i},'center', textH-50*(2-i), white);
            end
            Screen('Flip', theWindow);
        end
        
        wgdata.run_start(run_i) = GetSecs; % seed word timestamp
        wgdata.run_timestamp(run_i) = datetime('now');
        
        % Showing seed word, beeping, recording
        for response_n = 1:response_repeat
            
            % seed word for 2s
            if response_n == 1
                Screen('FillRect', theWindow, bgcolor, window_rect);
                Screen('TextSize', theWindow, fontsize*2); % emphasize
                DrawFormattedText(theWindow, double(seed{run_i}),'center', textH, orange);
                Screen('Flip', theWindow);
                waitsec_fromstarttime(wgdata.run_start(run_i), 2);
            end
            
            Screen('FillRect', theWindow, bgcolor, window_rect);
            Screen('Flip', theWindow);
            
            % beeping
            beep = MakeBeep(1000,.2);
            Snd('Play',beep);
            wgdata.beeptime_from_start(response_n,run_i) = GetSecs-wgdata.run_start(run_i);
            
            % cross for 1s
            Screen('FillRect', theWindow, bgcolor, window_rect);
            Screen('TextSize', theWindow, fontsize*1.2); % emphasize
            DrawFormattedText(theWindow, '+', 'center', textH, white);
            Screen('Flip', theWindow);
            waitsec_fromstarttime(wgdata.run_start(run_i), time_fromstart(response_n)-1)
            
            % blank for 1.5s
            Screen('FillRect', theWindow, bgcolor, window_rect);
            Screen('Flip', theWindow);
            waitsec_fromstarttime(wgdata.run_start(run_i), time_fromstart(response_n))
        end
    end
    wgdata.end_time = datetime('now');
    save(wgdata.wordfile, 'wgdata', '-append');
    
    
    %% RUN END MESSAGE
    Screen(theWindow, 'FillRect', bgcolor, window_rect);
    DrawFormattedText(theWindow, run_end_prompt, 'center', textH, white);
    Screen('Flip', theWindow);
    
    
    % close screen
    WaitSecs(3);
    
    ShowCursor; %unhide mouse
    Screen('CloseAll'); %relinquish screen control
    
    
catch err
    % ERROR
    disp(err);
    for i = 1:numel(err.stack)
        disp(err.stack(i));
    end
    abort_experiment('error');
end

end



%% == SUBFUNCTIONS ==============================================

function abort_experiment(varargin)

% ABORT the experiment
%
% abort_experiment(varargin)

str = 'Experiment aborted.';

for i = 1:length(varargin)
    if ischar(varargin{i})
        switch varargin{i}
            % functional commands
            case {'error'}
                str = 'Experiment aborted by error.';
            case {'manual'}
                str = 'Experiment aborted by the experimenter.';
        end
    end
end


ShowCursor; %unhide mouse
Screen('CloseAll'); %relinquish screen control
disp(str); %present this text in command window

end