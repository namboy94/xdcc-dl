package xdcc.downloader.bots.listeners;

import org.pircbotx.Configuration;
import org.pircbotx.PircBotX;
import org.pircbotx.User;
import org.pircbotx.dcc.ReceiveFileTransfer;
import org.pircbotx.hooks.Event;
import org.pircbotx.hooks.ListenerAdapter;
import org.pircbotx.hooks.events.IncomingFileTransferEvent;
import org.pircbotx.hooks.events.JoinEvent;
import org.pircbotx.hooks.types.GenericMessageEvent;
import xdcc.downloader.objects.Pack;
import xdcc.downloader.objects.Server;
import xdcc.downloader.parsers.Terminal;

import java.io.File;
import java.net.Socket;

public class MainListener extends ListenerAdapter {

    String nick;
    Pack[] botPack;
    String downLoadDirectory;
    int counter;

    public MainListener(String nick, Pack[] botPacks, String downLoadDirectory) {
        this.nick = nick;
        this.botPack = botPacks;
        this.downLoadDirectory = downLoadDirectory;
        this.counter = 0;
    }

    @Override
    public void onJoin(JoinEvent event) throws Exception {
        if (event.getUser().getNick().equals(nick)) {
            event.getBot().sendIRC().message(this.botPack[0].getPackArray()[0], this.botPack[0].getPackArray()[1]);
            counter++;
        }
    }

    @Override
    public void onIncomingFileTransfer(IncomingFileTransferEvent event) throws Exception {
        File file = new File(downLoadDirectory + event.getSafeFilename());
        if (file.exists()) {
            Socket socket = new Socket(event.getAddress(), event.getPort());
            Configuration configuration = event.getBot().getConfiguration();
            User user = event.getUser();
            ReceiveFileTransfer transferer = new ReceiveFileTransfer(configuration, socket, user, file, file.length(), event.getFilesize());
            Terminal.printLine(downLoadDirectory + event.getSafeFilename());
            Terminal.printLine("" + transferer.getStartPosition());
            transferer.transfer();
        }
        else {
            ReceiveFileTransfer transferer = event.accept(file);
            Terminal.printLine(downLoadDirectory + event.getSafeFilename());
            Terminal.printLine("" + transferer.getStartPosition());
            transferer.transfer();
        }
        
        if (this.counter < botPack.length) {
            event.getBot().sendIRC().message("Start " + this.botPack[counter].getPackArray()[0], this.botPack[counter].getPackArray()[1]);
            this.counter++;
        }
        else {
            event.getBot().close();
        }
        
    }
    //OK : Ginpachi-Sensei!~Gin@oshiete.ginpachi.sensei PRIVMSG nambo0 :DCC SEND "[HorribleSubs] Log Horizon 2 - 24 [480p].mkv" 623926352 53842 159058390
    //NOT OK: Ginpachi-Sensei!~Gin@oshiete.ginpachi.sensei PRIVMSG nambo0 :DCC ACCEPT "[HorribleSubs] Log Horizon 2 - 24 [480p].mkv" 44950 82390684
}