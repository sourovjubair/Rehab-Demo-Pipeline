%  Create and then hide the UI as it is being constructed.
f = figure('Visible','off','Position',[300,300,1024,500]);
0
%  Construct the components.
hstart = uicontrol('Style','pushbutton','String','Start',...
   'Position',[50,424+25,70,25],...
   'Callback',{@startbutton_Callback});
hstop = uicontrol('Style','pushbutton','String','Stop',...
   'Position',[150,424+25,70,25],...
   'Callback',{@stopbutton_Callback});
ha = axes('Units','pixels','Position',[0,0,512,424]);
ha1 = axes('Units','pixels','Position',[513,0,512,424]);

% Make the UI visible.
f.Visible = 'on';   

function startbutton_Callback(source,eventdata) 
% Display surf plot of the currently selected data.
record = 1;
end
function stopbutton_Callback(source,eventdata) 
% Display surf plot of the currently selected data.
record = 0;
end