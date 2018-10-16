-- description: Update current item amount based on the latest bid
PRAGMA foreign_keys = ON;
drop trigger if exists trigger13_add;
create trigger trigger13_add
after insert on Bids
begin
update Items set Number_of_Bids = Number_of_Bids+1
where ItemID = new.ItemID;
end;