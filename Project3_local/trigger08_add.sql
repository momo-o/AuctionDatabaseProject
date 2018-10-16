-- description: Update current item amount based on the latest bid
PRAGMA foreign_keys = ON;
drop trigger if exists trigger08_add;
create trigger trigger08_add
after insert on Bids
begin
update Items set currently = new.amount
where ItemID = new.ItemID;
end;